from pseudonymize.memory.bloom import BloomFilter


def test_bloom_filter() -> None:
    words = ["hope", "trust", "faith", "love", "jump"]
    bf = BloomFilter.from_words(words)

    for word in words:
        assert word in bf

    assert "Jonathan" not in bf
    assert "Doe" not in bf


def test_cached_miss_is_invalidated_after_add() -> None:
    bf = BloomFilter(100)
    for word in ("new-entry", "Élodie", "東京", ""):
        assert word not in bf
        bf.add(word)
        assert word in bf
        bf.add(word)
        assert word in bf


def test_mutation_preserves_previous_members() -> None:
    bf = BloomFilter.from_words(iter(["alpha", "beta"]))
    assert "alpha" in bf
    assert "gamma" not in bf
    bf.add("gamma")
    assert all(word in bf for word in ("alpha", "beta", "gamma"))


def test_small_filter_has_at_least_one_bit() -> None:
    bf = BloomFilter(1, error_rate=0.99)
    assert "entry" not in bf
    bf.add("entry")
    assert "entry" in bf


def test_invalid_filter_parameters() -> None:
    import pytest

    for capacity in (0, -1):
        with pytest.raises(ValueError, match="capacity must be positive"):
            BloomFilter(capacity)
    for rate in (0.0, -0.1, 1.0, 2.0, float("nan"), float("inf")):
        with pytest.raises(ValueError, match="error_rate must be between 0 and 1"):
            BloomFilter(10, rate)
