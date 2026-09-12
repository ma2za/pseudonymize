from pseudonymize.detectors.gazetteer import _load_dawg, _load_bloom

def test_load_dawg_missing() -> None:
    assert _load_dawg("does_not_exist.txt") is None

def test_load_bloom_missing() -> None:
    assert _load_bloom("does_not_exist.txt") is None
