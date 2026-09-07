from pseudonymize.memory.bloom import BloomFilter


def test_bloom_filter() -> None:
    words = ["hope", "trust", "faith", "love", "jump"]
    bf = BloomFilter.from_words(words)

    for word in words:
        assert word in bf

    assert "Jonathan" not in bf
    assert "Doe" not in bf
