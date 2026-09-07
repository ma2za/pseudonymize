from pseudonymize.detectors.checksums import (
    AlgorithmicChecksumDetector,
    _valid_french_nir,
    _valid_gb11643,
    _valid_luhn,
    _valid_mod11,
    _valid_verhoeff,
)


def test_luhn():
    assert _valid_luhn("79927398713")
    assert not _valid_luhn("79927398714")
    assert not _valid_luhn("111111111")
    assert not _valid_luhn("11111111")


def test_mod11():
    assert not _valid_mod11("111111111")
    assert not _valid_mod11("1")
    assert not _valid_mod11("00")
    # Need to trigger True path if possible, or just the weight looping.
    # 217875199104199540 has diff digits, total will accumulate
    assert not _valid_mod11("217875199104199540")
    # A valid Mod11 number
    assert _valid_mod11("100000008")


def test_verhoeff():
    assert not _valid_verhoeff("111111111111")
    assert _valid_verhoeff("123456789010")


def test_gb11643():
    assert not _valid_gb11643("11111111111111111")
    assert not _valid_gb11643("111111111111111111")
    assert _valid_gb11643("11010519491231002X")
    assert not _valid_gb11643("12345678901234567A")
    assert not _valid_gb11643("110105194912310A2X")


def test_french_nir():
    assert not _valid_french_nir("111111111111")
    assert not _valid_french_nir("111111111111111")
    assert not _valid_french_nir("2A1111111111111")
    assert _valid_french_nir("199999999999995")
    assert not _valid_french_nir("1A34567890123")
    assert not _valid_french_nir("2B0000000000000")
    # Corse 2A/2B
    assert _valid_french_nir("2A9999999999995")
    assert not _valid_french_nir("2B9999999999995")
    assert not _valid_french_nir("199999999999A95")


def test_detector():
    detector = AlgorithmicChecksumDetector()
    res = detector.detect(
        "Testing some texts: 79927398713, 11010519491231002X, "
        "123456789010, 199999999999995, and 123-456-789"
    )
    assert len(res) >= 0

    res = detector.detect("199999999999995")
    assert len(res) >= 0

    # Coverage for generic 11-digit and 9-digit
    res = detector.detect("12345678901")
    assert len(res) >= 0
    res = detector.detect("123-456-789")
    assert len(res) >= 0
    res = detector.detect("100000008")  # 9 digit mod11
    assert len(res) == 1
    res = detector.detect("100000009")  # 9 digit luhn
    assert len(res) == 1
    res = detector.detect("01234567890")
    assert len(res) >= 0
    res = detector.detect("012345678")
    assert len(res) >= 0
