from collections.abc import Iterable


class TrieNode:
    __slots__ = ("children", "is_terminal")

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_terminal: bool = False


class DAWG:
    """A minimal Trie/DAWG interface for High-Density Gazetteers."""

    __slots__ = ("_root",)

    def __init__(self) -> None:
        self._root = TrieNode()

    @classmethod
    def from_words(cls, words: Iterable[str]) -> "DAWG":
        dawg = cls()
        for word in words:
            dawg.add(word)
        return dawg

    def add(self, word: str) -> None:
        node = self._root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_terminal = True

    def __contains__(self, word: str) -> bool:
        node = self._root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_terminal
