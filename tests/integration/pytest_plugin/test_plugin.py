import pytest

from pseudonymize.pytest.plugin import assert_no_pii, assert_no_values


def test_assert_no_pii_passes() -> None:
    assert_no_pii("Hello world. The weather is nice.")


def test_assert_no_pii_fails() -> None:
    with pytest.raises(AssertionError, match="PII boundary violation: detected 1x EMAIL"):
        assert_no_pii("Contact bob@example.com.")


def test_assert_no_values_passes() -> None:
    assert_no_values("Hello Alice", ["Bob", "Charlie"])


def test_assert_no_values_fails() -> None:
    with pytest.raises(AssertionError, match="Canary boundary violation: 2 seeded values leaked"):
        assert_no_values("Hello Bob and Charlie", ["Bob", "Charlie"])
