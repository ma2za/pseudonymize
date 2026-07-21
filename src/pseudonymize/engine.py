import re
from collections.abc import Callable, Mapping, Sequence
from typing import TypeAlias, cast

from pseudonymize.detectors import DEFAULT_DETECTORS, Detector
from pseudonymize.exceptions import UnsupportedDataError
from pseudonymize.policy import Policy
from pseudonymize.result import Detection, Replacement, Result
from pseudonymize.spans import resolve_overlaps
from pseudonymize.transforms import HmacTransformer, Transformer

Data: TypeAlias = (
    str | int | float | bool | None | dict[str, "Data"] | list["Data"] | tuple["Data", ...]
)
Serializer: TypeAlias = Callable[[object], Data]
_TOKEN = re.compile(r"<PZ1:[A-Z_]+:[A-Z2-7]{16}>")


class Pseudonymizer:
    def __init__(
        self,
        *,
        key: bytes,
        namespace: str = "default",
        policy: Policy | None = None,
        detectors: Sequence[Detector] = DEFAULT_DETECTORS,
        transformer: Transformer | None = None,
    ) -> None:
        self.policy = policy or Policy.default()
        self.detectors = tuple(detectors)
        self.transformer = transformer or HmacTransformer(key, namespace)

    def detect(self, text: str) -> tuple[Detection, ...]:
        protected = tuple((match.start(), match.end()) for match in _TOKEN.finditer(text))
        detections = (
            detection
            for detector in self.detectors
            for detection in detector.detect(text)
            if detection.entity_type in self.policy.entity_types
            and detection.confidence >= self.policy.minimum_confidence
            and not any(
                detection.start < token_end and token_start < detection.end
                for token_start, token_end in protected
            )
        )
        return resolve_overlaps(detections, self.policy.detector_priority)

    def process(self, text: str) -> Result:
        detections = self.detect(text)
        tokens = [
            self.transformer.transform(text[detection.start : detection.end], detection)
            for detection in detections
        ]
        output = text
        for detection, token in reversed(tuple(zip(detections, tokens, strict=True))):
            output = output[: detection.start] + token + output[detection.end :]
        replacements: list[Replacement] = []
        offset = 0
        for detection, token in zip(detections, tokens, strict=True):
            output_start = detection.start + offset
            output_end = output_start + len(token)
            replacements.append(Replacement(detection, output_start, output_end, token))
            offset += len(token) - (detection.end - detection.start)
        return Result(output, tuple(replacements))

    def process_batch(self, texts: Sequence[str]) -> tuple[Result, ...]:
        return tuple(self.process(text) for text in texts)

    def process_data(self, data: Data | object, *, serializer: Serializer | None = None) -> Data:
        return self._process_data(data, (), serializer)

    def _process_data(
        self, data: Data | object, path: tuple[str, ...], serializer: Serializer | None
    ) -> Data:
        if isinstance(data, str):
            return self.process(data).text if self.policy.allows_path(path) else data
        if data is None or isinstance(data, (bool, int, float)):
            return data
        if isinstance(data, Mapping):
            if not all(isinstance(key, str) for key in data):
                raise UnsupportedDataError("dictionary keys must be strings")
            return {
                cast(str, key): self._process_data(value, (*path, cast(str, key)), serializer)
                for key, value in data.items()
            }
        if isinstance(data, list):
            return [
                self._process_data(value, (*path, str(index)), serializer)
                for index, value in enumerate(data)
            ]
        if isinstance(data, tuple):
            return tuple(
                self._process_data(value, (*path, str(index)), serializer)
                for index, value in enumerate(data)
            )
        if serializer is not None:
            return self._process_data(serializer(data), path, None)
        raise UnsupportedDataError(f"unsupported data type: {type(data).__name__}")
