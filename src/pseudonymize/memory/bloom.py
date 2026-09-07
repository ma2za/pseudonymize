import hashlib
import math
from collections.abc import Collection, Iterable


class BloomFilter:
    __slots__ = ("_bit_array", "_hash_count", "_size")

    def __init__(self, capacity: int, error_rate: float = 0.001) -> None:
        self._size = self._get_size(capacity, error_rate)
        self._hash_count = self._get_hash_count(self._size, capacity)
        self._bit_array = bytearray((self._size + 7) // 8)

    @classmethod
    def from_words(cls, words: Iterable[str], error_rate: float = 0.001) -> "BloomFilter":
        if isinstance(words, Collection):
            capacity = len(words)
        else:
            words = list(words)
            capacity = len(words)

        bf = cls(max(capacity, 1), error_rate)
        for word in words:
            bf.add(word)
        return bf

    def _hash(self, item: str, seed: int) -> int:
        h = hashlib.sha256()
        h.update(item.encode("utf-8"))
        h.update(seed.to_bytes(4, "big"))
        return int.from_bytes(h.digest(), "big")

    def add(self, item: str) -> None:
        for i in range(self._hash_count):
            digest = self._hash(item, i) % self._size
            self._bit_array[digest // 8] |= 1 << (digest % 8)

    def __contains__(self, item: str) -> bool:
        for i in range(self._hash_count):
            digest = self._hash(item, i) % self._size
            if not (self._bit_array[digest // 8] & (1 << (digest % 8))):
                return False
        return True

    @staticmethod
    def _get_size(n: int, p: float) -> int:
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @staticmethod
    def _get_hash_count(m: int, n: int) -> int:
        k = (m / n) * math.log(2)
        return max(1, int(k))
