import pytest

from pseudonymize.detectors.context import ContextualIdDetector
from pseudonymize.result import EntityType


@pytest.mark.parametrize(
    "text",
    [
        # A label alone is not evidence: an ordinary word sat where the
        # identifier belongs and was reported as personal data.
        "Please provide identification number before Tuesday",
        "The applicant Jonathan submitted forms.",
        "The id must be alphanumeric and unique.",
        # Triggers that only ever co-occurred with an identifier in one corpus.
        "We approved a budget of 1500000000000 lire.",
        "A contribution of 1234567890123 was recorded.",
        "Your school 100200 is nearby.",
        "Our office at 123456 Ocean Drive is open.",
        # Labels that are ordinary English words outside an identifier context.
        "The serial drama continues tonight.",
        "Reference the attached document carefully.",
    ],
)
def test_context_detector_ignores_prose_without_an_identifier(text: str) -> None:
    assert ContextualIdDetector().detect(text) == []


@pytest.mark.parametrize(
    ("text", "value", "entity_type"),
    [
        ("Passport No: X1234567 was issued in Rome.", "X1234567", EntityType.NATIONAL_ID),
        ("Tax ID: IT12345678901 for the invoice.", "IT12345678901", EntityType.TAX_ID),
        ("National ID 990011223 on file.", "990011223", EntityType.NATIONAL_ID),
        ("Ticket number: TK-9928311 is open.", "TK-9928311", EntityType.NATIONAL_ID),
        ("Zip code: 20144 in Milan.", "20144", EntityType.LOCATION),
        ("Account number 4455661234 was closed.", "4455661234", EntityType.SECRET),
        (
            "Credit card number 4111111111111111 declined.",
            "4111111111111111",
            EntityType.PAYMENT_CARD,
        ),
        ("Driver's licence no AB1234567 expires soon.", "AB1234567", EntityType.NATIONAL_ID),
        ("Mã số thuế 0101243150 đã đăng ký.", "0101243150", EntityType.TAX_ID),
        ("护照号 E12345678 已过期。", "E12345678", EntityType.NATIONAL_ID),
    ],
)
def test_context_detector_still_reads_labelled_identifiers(
    text: str, value: str, entity_type: EntityType
) -> None:
    detections = ContextualIdDetector().detect(text)
    assert [(text[item.start : item.end], item.entity_type) for item in detections] == [
        (value, entity_type)
    ]


def test_context_detector_requires_a_digit_in_alphanumeric_identifiers() -> None:
    """An all-letter word after a label is a word, not an identifier."""
    assert ContextualIdDetector().detect("Passport No: ABCDEFGH was issued.") == []
    assert ContextualIdDetector().detect("Passport No: ABCDEF1H was issued.")
