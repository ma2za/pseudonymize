import pytest

from pseudonymize import EntityType
from pseudonymize.detectors.email import EmailDetector
from pseudonymize.detectors.iban import IbanDetector, _valid_mod97
from pseudonymize.detectors.ip_address import IpAddressDetector
from pseudonymize.detectors.payment_card import PaymentCardDetector, _valid_luhn
from pseudonymize.detectors.phone import PhoneDetector
from pseudonymize.detectors.secret import SecretDetector
from pseudonymize.detectors.url import UrlDetector


@pytest.mark.parametrize(
    ("detector", "text", "entity_type", "value"),
    [
        (EmailDetector(), "Contact maria@example.com.", EntityType.EMAIL, "maria@example.com"),
        (
            IpAddressDetector(),
            "Hosts 192.168.1.1 and 2001:db8::1.",
            EntityType.IP_ADDRESS,
            "192.168.1.1",
        ),
        (
            PaymentCardDetector(),
            "Card 4111 1111 1111 1111.",
            EntityType.PAYMENT_CARD,
            "4111 1111 1111 1111",
        ),
        (
            IbanDetector(),
            "IBAN GB82 WEST 1234 5698 7654 32.",
            EntityType.IBAN,
            "GB82 WEST 1234 5698 7654 32",
        ),
        (PhoneDetector(), "Call +39 333 123 4567.", EntityType.PHONE, "+39 333 123 4567"),
        (SecretDetector(), "api_key='abcdefghijk12345'", EntityType.SECRET, "abcdefghijk12345"),
        (UrlDetector(), "See https://me:pass@example.com/a", EntityType.URL_CREDENTIAL, "me:pass"),
        (
            UrlDetector(),
            "See https://example.com/?token=secret123",
            EntityType.URL_CREDENTIAL,
            "secret123",
        ),
    ],
)
def test_valid_candidates(detector: object, text: str, entity_type: EntityType, value: str) -> None:
    detections = detector.detect(text)  # type: ignore[attr-defined]
    assert any(
        detection.entity_type is entity_type and text[detection.start : detection.end] == value
        for detection in detections
    )


@pytest.mark.parametrize(
    ("detector", "text"),
    [
        (EmailDetector(), "not-an-email@example"),
        (IpAddressDetector(), "999.999.999.999"),
        (PaymentCardDetector(), "4111 1111 1111 1112"),
        (IbanDetector(), "GB82 WEST 1234 5698 7654 33"),
        (PhoneDetector(), "12345678"),
        (UrlDetector(), "https://example.com/?page=1"),
        (SecretDetector(), "token=short"),
    ],
)
def test_invalid_candidates(detector: object, text: str) -> None:
    assert detector.detect(text) == []  # type: ignore[attr-defined]


def test_validators_reject_repeated_or_malformed_values() -> None:
    assert not _valid_luhn("0000 0000 0000 0000")
    assert not _valid_luhn("123")
    assert not _valid_mod97("GB82")
    assert _valid_luhn("5555555555554444")


def test_phone_rejects_repeated_digits() -> None:
    assert PhoneDetector().detect("+11 111 111 111") == []


@pytest.mark.parametrize("suffix", [".", '."', ".)", ".\n"])
def test_ip_address_accepts_sentence_terminators(suffix: str) -> None:
    text = f"Host 192.0.2.10{suffix}"
    detections = IpAddressDetector().detect(text)
    assert len(detections) == 1
    assert text[detections[0].start : detections[0].end] == "192.0.2.10"


@pytest.mark.parametrize("text", ["192.0.2.10.5", "192.0.2.10.example"])
def test_ip_address_rejects_partial_dotted_values(text: str) -> None:
    assert IpAddressDetector().detect(text) == []


def test_url_detects_username_and_empty_sensitive_value_safely() -> None:
    text = "https://user@example.com/?token=&api_key=present"
    values = [text[item.start : item.end] for item in UrlDetector().detect(text)]
    assert values == ["user", "present"]


def test_secret_provider_patterns() -> None:
    values = [
        "AKIAABCDEFGHIJKLMNOP",
        "ghp_abcdefghijklmnopqrstuvwxyzABCDEFGHIJ",
        "sk-abcdefghijklmnopqrstuvwxyz",
    ]
    for value in values:
        assert SecretDetector().detect(value)
