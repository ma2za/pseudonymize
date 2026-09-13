from pseudonymize.detectors.gazetteer import _load_bloom, _load_dawg


def test_load_dawg_missing() -> None:
    assert _load_dawg("does_not_exist.txt") is None


def test_load_bloom_missing() -> None:
    assert _load_bloom("does_not_exist.txt") is None
