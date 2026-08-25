import os
import re
import tempfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from types import MappingProxyType
from typing import TypeAlias, cast

from pseudonymize.adapters import InputAdapter, OutputAdapter
from pseudonymize.backends import (
    BackendCapabilities,
    DetectionBackend,
    RulesBackend,
    backend_capabilities,
    leaf_backends,
)
from pseudonymize.backends.base import invoke_backend
from pseudonymize.detectors import DEFAULT_DETECTORS, Detector
from pseudonymize.document import (
    ContentBlock,
    Document,
    JSONPathLocation,
    TextOffsetLocation,
)
from pseudonymize.exceptions import (
    AdapterContractError,
    AdapterExecutionError,
    FileProcessingError,
    InvalidKeyError,
    UnsupportedDataError,
    UnsupportedFormatError,
)
from pseudonymize.formats import (
    INSPECTION_ONLY_FORMATS,
    BuiltinFileAdapter,
    FileFormat,
    select_file_format,
)
from pseudonymize.policy import Policy
from pseudonymize.processing import (
    DetectionReport,
    ProcessingResult,
    ProcessingStatistics,
)
from pseudonymize.resolution import EntityResolver, ExactEntityResolver, ResolvedEntity
from pseudonymize.result import Detection, EntityType, Replacement, Result
from pseudonymize.spans import resolve_overlaps
from pseudonymize.transforms import (
    Alias,
    AliasAssigner,
    AliasContext,
    DeterministicAliasAssigner,
    GenericAliasAssigner,
    NumberedAliasAssigner,
    PlaceholderTransformer,
    RedactTransformer,
    TransformationMode,
    Transformer,
)

Data: TypeAlias = (
    str | int | float | bool | dict[str, "Data"] | list["Data"] | tuple["Data", ...] | None
)
Serializer: TypeAlias = Callable[[object], Data]
_ENTITY_NAMES = "|".join(re.escape(entity_type.value) for entity_type in EntityType)
_PLACEHOLDER = re.compile(
    rf"<(?:{_ENTITY_NAMES})(?:_(?:\d+|[A-Z2-7]{{6,}}))?>|"
    rf"<PZ1:(?:{_ENTITY_NAMES}):[A-Z2-7]{{16}}>|"
    rf"\[REDACTED(?:_(?:{_ENTITY_NAMES}))?\]"
)


class Pseudonymizer:
    def __init__(
        self,
        *,
        mode: TransformationMode | str = TransformationMode.NUMBERED,
        key: bytes | None = None,
        namespace: str = "default",
        policy: Policy | None = None,
        detectors: Sequence[Detector] | None = None,
        backends: Sequence[DetectionBackend] | None = None,
        resolver: EntityResolver | None = None,
        assigner: AliasAssigner | None = None,
        transformer: Transformer | None = None,
        typed_redaction: bool = False,
    ) -> None:
        if detectors is not None and backends is not None:
            raise ValueError("configure detectors or backends, not both")
        self.mode = TransformationMode(mode)
        if assigner is not None and (key is not None or namespace != "default"):
            raise ValueError("key and namespace must be configured by a custom alias assigner")
        if typed_redaction and self.mode is not TransformationMode.REDACTED:
            raise ValueError("typed_redaction is valid only in redacted mode")
        self.policy = policy or Policy.default()
        configured_detectors = DEFAULT_DETECTORS if detectors is None else detectors
        self.backends = (
            tuple(backends) if backends is not None else (RulesBackend(configured_detectors),)
        )
        self.backends = leaf_backends(self.backends)
        self.resolver = resolver or ExactEntityResolver()
        self.assigner = assigner or _assigner_for(self.mode, key, namespace)
        self.transformer = transformer or _transformer_for(self.mode, typed_redaction)

    def detect(self, text: str) -> tuple[Detection, ...]:
        block = ContentBlock("text", text, TextOffsetLocation(0, len(text)))
        return self._detect_block(block, _OperationStatistics())

    def _detect_block(
        self, block: ContentBlock, statistics: "_OperationStatistics"
    ) -> tuple[Detection, ...]:
        statistics.blocks_processed += 1

        # Obfuscation removal: strip zero-width characters and BiDi overrides
        # while keeping a mapping to original indices.
        # U+200B to U+200F (ZWSP, ZWNJ, ZWJ, LRM, RLM), U+202A to U+202E (LRE, RLE, PDF, LRO, RLO),
        # U+FEFF (BOM)
        obfuscation_chars = frozenset(
            "\u200b\u200c\u200d\u200e\u200f\u202a\u202b\u202c\u202d\u202e\ufeff"
        )
        original_text = block.text
        if any(c in obfuscation_chars for c in original_text):
            clean_chars: list[str] = []
            original_indices: list[int] = []
            for i, char in enumerate(original_text):
                if char not in obfuscation_chars:
                    clean_chars.append(char)
                    original_indices.append(i)
            original_indices.append(len(original_text))  # For the end boundary

            clean_text = "".join(clean_chars)
            # Create a shallow copy of the block with the clean text for the backends
            from dataclasses import replace

            clean_block = replace(block, text=clean_text)
        else:
            clean_block = block
            original_indices = []  # Empty means 1:1 mapping

        candidates: list[Detection] = []
        for backend in self.backends:
            capabilities = backend_capabilities(backend)
            if not capabilities.entity_types.intersection(self.policy.entity_types):
                continue
            detections = invoke_backend(backend, clean_block, self.policy)
            statistics.record_backend(capabilities)

            if original_indices:
                mapped_detections = []
                for det in detections:
                    # Map back to original bounds
                    mapped_start = original_indices[det.start]
                    mapped_end = original_indices[det.end]
                    # Also map the value if the backend provided it
                    original_text[mapped_start:mapped_end]

                    mapped_detections.append(
                        Detection(
                            entity_type=det.entity_type,
                            start=mapped_start,
                            end=mapped_end,
                            confidence=det.confidence,
                            detector=det.detector,
                            backend=det.backend,
                        )
                    )
                candidates.extend(mapped_detections)
            else:
                candidates.extend(detections)

        text = block.text
        protected = tuple((match.start(), match.end()) for match in _PLACEHOLDER.finditer(text))
        filtered = (
            detection
            for detection in candidates
            if detection.entity_type in self.policy.entity_types
            and detection.confidence >= self.policy.minimum_confidence
            and not any(
                detection.start < token_end and token_start < detection.end
                for token_start, token_end in protected
            )
        )
        return resolve_overlaps(filtered, self.policy.detector_priority)

    def process(self, text: str, *, include_mapping: bool = False) -> Result:
        return self._process(text, AliasContext(), include_mapping)

    def process_with_report(self, text: str) -> ProcessingResult[str]:
        statistics = _OperationStatistics()
        reports: list[DetectionReport] = []
        block = ContentBlock("text", text, TextOffsetLocation(0, len(text)))
        result = self._process_block(block, AliasContext(), False, statistics, reports)
        return ProcessingResult(result.text, tuple(reports), statistics.finish(reports))

    def process_batch(
        self, texts: Sequence[str], *, include_mapping: bool = False
    ) -> tuple[Result, ...]:
        context = AliasContext()
        return tuple(self._process(text, context, include_mapping) for text in texts)

    def process_data(self, data: Data | object, *, serializer: Serializer | None = None) -> Data:
        return self._process_data(
            data, (), serializer, AliasContext(), _OperationStatistics(), [], [0]
        )

    def process_data_with_report(
        self, data: Data | object, *, serializer: Serializer | None = None
    ) -> ProcessingResult[Data]:
        statistics = _OperationStatistics()
        reports: list[DetectionReport] = []
        output = self._process_data(data, (), serializer, AliasContext(), statistics, reports, [0])
        return ProcessingResult(output, tuple(reports), statistics.finish(reports))

    def process_document(self, document: Document) -> ProcessingResult[Document]:
        statistics = _OperationStatistics()
        reports: list[DetectionReport] = []
        context = AliasContext()
        blocks: list[ContentBlock] = []
        for block in document.blocks:
            if self._allows_block(block):
                result = self._process_block(block, context, False, statistics, reports)
                blocks.append(replace(block, text=result.text))
            else:
                statistics.blocks_processed += 1
                blocks.append(block)
        output = replace(document, blocks=tuple(blocks))
        return ProcessingResult(output, tuple(reports), statistics.finish(reports))

    def inspect_document(self, document: Document) -> ProcessingResult[None]:
        statistics = _OperationStatistics()
        reports: list[DetectionReport] = []
        for block in document.blocks:
            if self._allows_block(block):
                detections = self._detect_block(block, statistics)
                reports.extend(_detection_reports(block, detections))
            else:
                statistics.blocks_processed += 1
        return ProcessingResult(None, tuple(reports), statistics.finish(reports))

    def process_file(
        self,
        source: str | os.PathLike[str],
        destination: str | os.PathLike[str] | None = None,
        *,
        format: FileFormat | str | None = None,
        encoding: str | None = None,
        overwrite: bool = False,
        input_adapter: InputAdapter[Path] | None = None,
        output_adapter: OutputAdapter | None = None,
    ) -> ProcessingResult[Path]:
        source_path = Path(source)
        selected_input, selected_output = _processing_adapters(
            source_path,
            format,
            encoding,
            input_adapter,
            output_adapter,
        )
        destination_path = (
            Path(destination)
            if destination is not None
            else source_path.with_name(f"{source_path.stem}.safe{source_path.suffix}")
        )
        if source_path.resolve() == destination_path.resolve():
            raise ValueError("file processing never overwrites its source")
        if destination_path.exists() and not overwrite:
            raise FileExistsError("destination already exists")
        processed = self.process_document(_extract_document(selected_input, source_path))
        rendered = _render_document(selected_output, processed.output)
        try:
            _atomic_write(destination_path, rendered, overwrite)
        except FileExistsError:
            raise FileExistsError("destination already exists") from None
        except Exception:
            raise FileProcessingError("atomic output publication failed") from None
        return ProcessingResult(
            destination_path,
            processed.detections,
            processed.statistics,
            processed.warnings,
        )

    def inspect_file(
        self,
        source: str | os.PathLike[str],
        *,
        format: FileFormat | str | None = None,
        encoding: str | None = None,
        input_adapter: InputAdapter[Path] | None = None,
    ) -> ProcessingResult[None]:
        source_path = Path(source)
        selected_input = _inspection_adapter(source_path, format, encoding, input_adapter)
        return self.inspect_document(_extract_document(selected_input, source_path))

    def new_scope(self) -> "ProcessingScope":
        return ProcessingScope(self)

    def _process(self, text: str, context: AliasContext, include_mapping: bool) -> Result:
        block = ContentBlock("text", text, TextOffsetLocation(0, len(text)))
        return self._process_block(block, context, include_mapping, _OperationStatistics(), [])

    def _process_block(
        self,
        block: ContentBlock,
        context: AliasContext,
        include_mapping: bool,
        statistics: "_OperationStatistics",
        reports: list[DetectionReport],
    ) -> Result:
        if include_mapping and self.mode not in {
            TransformationMode.NUMBERED,
            TransformationMode.DETERMINISTIC,
        }:
            raise ValueError("mappings are available only in numbered and deterministic modes")
        text = block.text
        detections = self._detect_block(block, statistics)
        entities = self.resolver.resolve(text, detections)
        aliases = tuple(self.assigner.assign(entity, context) for entity in entities)
        tokens = tuple(
            self.transformer.render(entity, alias)
            for entity, alias in zip(entities, aliases, strict=True)
        )
        segments: list[str] = []
        cursor = 0
        for entity, token in zip(entities, tokens, strict=True):
            detection = entity.detection
            segments.append(text[cursor : detection.start])
            segments.append(token)
            cursor = detection.end
        segments.append(text[cursor:])
        output = "".join(segments)
        replacements = _replacement_reports(entities, tokens)
        reports.extend(_replacement_detection_reports(block, replacements))
        mapping = _mapping(text, entities, aliases, tokens) if include_mapping else None
        return Result(output, replacements, mapping)

    def _process_data(
        self,
        data: Data | object,
        path: tuple[str | int, ...],
        serializer: Serializer | None,
        context: AliasContext,
        statistics: "_OperationStatistics",
        reports: list[DetectionReport],
        block_counter: list[int],
    ) -> Data:
        if isinstance(data, str):
            block_id = f"block-{block_counter[0]:06d}"
            block_counter[0] += 1
            if not self.policy.allows_path(tuple(str(part) for part in path)):
                statistics.blocks_processed += 1
                return data
            block = ContentBlock(block_id, data, JSONPathLocation(path))
            return self._process_block(block, context, False, statistics, reports).text
        if data is None or isinstance(data, (bool, int, float)):
            return data
        if isinstance(data, Mapping):
            if not all(isinstance(key, str) for key in data):
                raise UnsupportedDataError("dictionary keys must be strings")
            return {
                cast(str, key): self._process_data(
                    value,
                    (*path, cast(str, key)),
                    serializer,
                    context,
                    statistics,
                    reports,
                    block_counter,
                )
                for key, value in data.items()
            }
        if isinstance(data, list):
            return [
                self._process_data(
                    value,
                    (*path, index),
                    serializer,
                    context,
                    statistics,
                    reports,
                    block_counter,
                )
                for index, value in enumerate(data)
            ]
        if isinstance(data, tuple):
            return tuple(
                self._process_data(
                    value,
                    (*path, index),
                    serializer,
                    context,
                    statistics,
                    reports,
                    block_counter,
                )
                for index, value in enumerate(data)
            )
        if serializer is not None:
            return self._process_data(
                serializer(data), path, None, context, statistics, reports, block_counter
            )
        raise UnsupportedDataError(f"unsupported data type: {type(data).__name__}")

    def _allows_block(self, block: ContentBlock) -> bool:
        location = block.location
        if isinstance(location, JSONPathLocation):
            return self.policy.allows_path(tuple(str(part) for part in location.path))
        return True


class ProcessingScope:
    def __init__(self, engine: Pseudonymizer) -> None:
        self._engine = engine
        self._context = AliasContext()

    def process(self, text: str, *, include_mapping: bool = False) -> Result:
        return self._engine._process(text, self._context, include_mapping)

    def process_data(self, data: Data | object, *, serializer: Serializer | None = None) -> Data:
        return self._engine._process_data(
            data, (), serializer, self._context, _OperationStatistics(), [], [0]
        )


@dataclass(slots=True)
class _OperationStatistics:
    blocks_processed: int = 0
    backend_invocations: int = 0
    local_block_calls: int = 0
    remote_block_calls: int = 0

    def record_backend(self, capabilities: BackendCapabilities) -> None:
        self.backend_invocations += 1
        if capabilities.remote:
            self.remote_block_calls += 1
        else:
            self.local_block_calls += 1

    def finish(self, reports: Sequence[DetectionReport]) -> ProcessingStatistics:
        return ProcessingStatistics(
            blocks_processed=self.blocks_processed,
            detections_found=len(reports),
            replacements_applied=sum(report.token is not None for report in reports),
            backend_invocations=self.backend_invocations,
            local_block_calls=self.local_block_calls,
            remote_block_calls=self.remote_block_calls,
        )


def _detection_reports(
    block: ContentBlock, detections: Sequence[Detection]
) -> tuple[DetectionReport, ...]:
    return tuple(_detection_report(block, detection) for detection in detections)


def _replacement_detection_reports(
    block: ContentBlock, replacements: Sequence[Replacement]
) -> tuple[DetectionReport, ...]:
    return tuple(
        _detection_report(block, replacement.detection, replacement.token)
        for replacement in replacements
    )


def _detection_report(
    block: ContentBlock, detection: Detection, token: str | None = None
) -> DetectionReport:
    return DetectionReport(
        entity_type=detection.entity_type,
        block_id=block.id,
        location=block.location,
        start=detection.start,
        end=detection.end,
        confidence=detection.confidence,
        backend=detection.backend,
        detector=detection.detector,
        token=token,
    )


def _atomic_write(destination: Path, rendered: bytes, overwrite: bool) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(rendered)
            stream.flush()
            os.fsync(stream.fileno())
        if overwrite:
            os.replace(temporary, destination)
        else:
            os.link(temporary, destination)
            temporary.unlink()
    finally:
        if temporary.exists():
            temporary.unlink()


def _extract_document(input_adapter: InputAdapter[Path], source: Path) -> Document:
    try:
        document = input_adapter.extract(source)
    except AdapterExecutionError:
        if isinstance(input_adapter, BuiltinFileAdapter):
            raise
        raise AdapterExecutionError("input adapter failed during extraction") from None
    except Exception:
        raise AdapterExecutionError("input adapter failed during extraction") from None
    if not isinstance(document, Document):
        raise AdapterContractError("input adapter must extract a Document")
    return document


def _processing_adapters(
    source: Path,
    format: FileFormat | str | None,
    encoding: str | None,
    input_adapter: InputAdapter[Path] | None,
    output_adapter: OutputAdapter | None,
) -> tuple[InputAdapter[Path], OutputAdapter]:
    if input_adapter is None and output_adapter is None:
        selected_format = select_file_format(source, format)
        if selected_format in INSPECTION_ONLY_FORMATS:
            raise UnsupportedFormatError(
                f"{selected_format.value} supports inspection only; "
                "use inspect_file or supply custom adapters"
            )
        if selected_format in {FileFormat.DOCX, FileFormat.XLSX, FileFormat.PPTX, FileFormat.PDF}:
            if encoding is not None:
                raise ValueError("encoding applies only to text-based formats")
            if selected_format is FileFormat.PDF:
                from pseudonymize.inspection.pdf import PDFInspectionAdapter

                pdf_adapter = PDFInspectionAdapter()
                return pdf_adapter, pdf_adapter

            from pseudonymize.inspection.office import OfficeInspectionAdapter

            office_adapter = OfficeInspectionAdapter(selected_format)
            return office_adapter, office_adapter

        builtin_adapter = BuiltinFileAdapter(selected_format, encoding)
        return builtin_adapter, builtin_adapter
    if input_adapter is None or output_adapter is None:
        raise ValueError("custom file processing requires input and output adapters")
    if format is not None or encoding is not None:
        raise ValueError("custom adapters cannot be combined with format or encoding")
    return input_adapter, output_adapter


def _inspection_adapter(
    source: Path,
    format: FileFormat | str | None,
    encoding: str | None,
    input_adapter: InputAdapter[Path] | None,
) -> InputAdapter[Path]:
    if input_adapter is None:
        selected_format = select_file_format(source, format)
        if selected_format in INSPECTION_ONLY_FORMATS or selected_format in {
            FileFormat.DOCX,
            FileFormat.XLSX,
            FileFormat.PPTX,
            FileFormat.PDF,
        }:
            if encoding is not None:
                raise ValueError("encoding applies only to text-based formats")
            if selected_format in {FileFormat.PNG, FileFormat.JPEG}:
                from pseudonymize.inspection.image import ImageInspectionAdapter

                return ImageInspectionAdapter(selected_format)
            if selected_format is FileFormat.PDF:
                from pseudonymize.inspection.pdf import PDFInspectionAdapter

                return PDFInspectionAdapter()
            from pseudonymize.inspection.office import OfficeInspectionAdapter

            return OfficeInspectionAdapter(selected_format)
        return BuiltinFileAdapter(selected_format, encoding)
    if format is not None or encoding is not None:
        raise ValueError("custom adapters cannot be combined with format or encoding")
    return input_adapter


def _render_document(output_adapter: OutputAdapter, document: Document) -> bytes:
    try:
        rendered = output_adapter.render(document)
    except Exception:
        raise AdapterExecutionError("output adapter failed during rendering") from None
    if not isinstance(rendered, bytes):
        raise AdapterContractError("output adapter must render bytes")
    return rendered


def _assigner_for(mode: TransformationMode, key: bytes | None, namespace: str) -> AliasAssigner:
    if mode is TransformationMode.DETERMINISTIC:
        if key is None:
            raise InvalidKeyError("deterministic mode requires a key of at least 32 bytes")
        return DeterministicAliasAssigner(key, namespace)
    if key is not None:
        raise ValueError("key is only valid in deterministic mode")
    if namespace != "default":
        raise ValueError("namespace is only valid in deterministic mode")
    if mode is TransformationMode.NUMBERED:
        return NumberedAliasAssigner()
    return GenericAliasAssigner()


def _transformer_for(mode: TransformationMode, typed_redaction: bool) -> Transformer:
    if mode is TransformationMode.REDACTED:
        return RedactTransformer(typed_redaction)
    return PlaceholderTransformer()


def _replacement_reports(
    entities: Sequence[ResolvedEntity], tokens: Sequence[str]
) -> tuple[Replacement, ...]:
    replacements: list[Replacement] = []
    offset = 0
    for entity, token in zip(entities, tokens, strict=True):
        detection = entity.detection
        output_start = detection.start + offset
        output_end = output_start + len(token)
        replacements.append(Replacement(detection, output_start, output_end, token))
        offset += len(token) - (detection.end - detection.start)
    return tuple(replacements)


def _mapping(
    text: str,
    entities: Sequence[ResolvedEntity],
    aliases: Sequence[Alias],
    tokens: Sequence[str],
) -> Mapping[str, str]:
    values: dict[str, str] = {}
    for entity, alias, token in zip(entities, aliases, tokens, strict=True):
        if alias.identifier is not None:
            detection = entity.detection
            values.setdefault(token, text[detection.start : detection.end])
    return MappingProxyType(values)
