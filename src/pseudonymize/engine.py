import re
from collections.abc import Callable, Mapping, Sequence
from types import MappingProxyType
from typing import TypeAlias, cast

from pseudonymize.backends import DetectionBackend, RulesBackend
from pseudonymize.detectors import DEFAULT_DETECTORS, Detector
from pseudonymize.exceptions import InvalidKeyError, UnsupportedDataError
from pseudonymize.policy import Policy
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
    str | int | float | bool | None | dict[str, "Data"] | list["Data"] | tuple["Data", ...]
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
        self.resolver = resolver or ExactEntityResolver()
        self.assigner = assigner or _assigner_for(self.mode, key, namespace)
        self.transformer = transformer or _transformer_for(self.mode, typed_redaction)

    def detect(self, text: str) -> tuple[Detection, ...]:
        protected = tuple((match.start(), match.end()) for match in _PLACEHOLDER.finditer(text))
        detections = (
            detection
            for backend in self.backends
            for detection in backend.detect(text)
            if detection.entity_type in self.policy.entity_types
            and detection.confidence >= self.policy.minimum_confidence
            and not any(
                detection.start < token_end and token_start < detection.end
                for token_start, token_end in protected
            )
        )
        return resolve_overlaps(detections, self.policy.detector_priority)

    def process(self, text: str, *, include_mapping: bool = False) -> Result:
        return self._process(text, AliasContext(), include_mapping)

    def process_batch(
        self, texts: Sequence[str], *, include_mapping: bool = False
    ) -> tuple[Result, ...]:
        context = AliasContext()
        return tuple(self._process(text, context, include_mapping) for text in texts)

    def process_data(self, data: Data | object, *, serializer: Serializer | None = None) -> Data:
        return self._process_data(data, (), serializer, AliasContext())

    def new_scope(self) -> "ProcessingScope":
        return ProcessingScope(self)

    def _process(self, text: str, context: AliasContext, include_mapping: bool) -> Result:
        if include_mapping and self.mode not in {
            TransformationMode.NUMBERED,
            TransformationMode.DETERMINISTIC,
        }:
            raise ValueError("mappings are available only in numbered and deterministic modes")
        detections = self.detect(text)
        entities = self.resolver.resolve(text, detections)
        aliases = tuple(self.assigner.assign(entity, context) for entity in entities)
        tokens = tuple(
            self.transformer.render(entity, alias)
            for entity, alias in zip(entities, aliases, strict=True)
        )
        output = text
        for entity, token in reversed(tuple(zip(entities, tokens, strict=True))):
            detection = entity.detection
            output = output[: detection.start] + token + output[detection.end :]
        replacements = _replacement_reports(entities, tokens)
        mapping = _mapping(text, entities, aliases, tokens) if include_mapping else None
        return Result(output, replacements, mapping)

    def _process_data(
        self,
        data: Data | object,
        path: tuple[str, ...],
        serializer: Serializer | None,
        context: AliasContext,
    ) -> Data:
        if isinstance(data, str):
            return (
                self._process(data, context, False).text if self.policy.allows_path(path) else data
            )
        if data is None or isinstance(data, (bool, int, float)):
            return data
        if isinstance(data, Mapping):
            if not all(isinstance(key, str) for key in data):
                raise UnsupportedDataError("dictionary keys must be strings")
            return {
                cast(str, key): self._process_data(
                    value, (*path, cast(str, key)), serializer, context
                )
                for key, value in data.items()
            }
        if isinstance(data, list):
            return [
                self._process_data(value, (*path, str(index)), serializer, context)
                for index, value in enumerate(data)
            ]
        if isinstance(data, tuple):
            return tuple(
                self._process_data(value, (*path, str(index)), serializer, context)
                for index, value in enumerate(data)
            )
        if serializer is not None:
            return self._process_data(serializer(data), path, None, context)
        raise UnsupportedDataError(f"unsupported data type: {type(data).__name__}")


class ProcessingScope:
    def __init__(self, engine: Pseudonymizer) -> None:
        self._engine = engine
        self._context = AliasContext()

    def process(self, text: str, *, include_mapping: bool = False) -> Result:
        return self._engine._process(text, self._context, include_mapping)

    def process_data(self, data: Data | object, *, serializer: Serializer | None = None) -> Data:
        return self._engine._process_data(data, (), serializer, self._context)


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
