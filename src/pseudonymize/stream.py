import re
from collections.abc import Callable

from pseudonymize.result import Result

_SAFE_SPLIT_REGEX = re.compile(r"([.?!,;:]\s+|\n)")


class TextStreamProcessor:
    def __init__(self, process_fn: Callable[[str], Result], overlap_size: int = 100):
        self._process_fn = process_fn
        self._overlap_size = overlap_size
        self._buffer = ""
        self._context = ""

    def push(self, chunk: str) -> str:
        self._buffer += chunk

        split_idx = -1
        for match in _SAFE_SPLIT_REGEX.finditer(self._buffer):
            if match.end() <= len(self._buffer) - 20:
                split_idx = match.end()

        if split_idx <= 0:
            if len(self._buffer) > 4096:
                split_idx = self._buffer.rfind(" ", 0, 2048)
                if split_idx == -1:
                    split_idx = 2048
            else:
                return ""

        to_process = self._buffer[:split_idx]
        self._buffer = self._buffer[split_idx:]

        return self._process_segment(to_process)

    def flush(self) -> str:
        if self._buffer:
            res = self._process_segment(self._buffer)
            self._buffer = ""
            return res
        return ""

    def _process_segment(self, segment: str) -> str:
        if not segment:
            return ""

        text = self._context + segment
        result = self._process_fn(text)

        context_len = len(self._context)
        slice_idx = 0
        shift = 0

        for rep in result.replacements:
            if context_len <= rep.detection.start:
                slice_idx = context_len + shift
                break
            elif rep.detection.start < context_len < rep.detection.end:
                slice_idx = rep.output_end
                break
            shift += (rep.output_end - rep.output_start) - (rep.detection.end - rep.detection.start)
        else:
            slice_idx = context_len + shift

        self._context = text[-self._overlap_size :] if len(text) > self._overlap_size else text
        return result.text[slice_idx:]
