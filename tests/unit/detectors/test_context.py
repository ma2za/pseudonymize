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


@pytest.mark.parametrize(
    ("text", "value", "entity_type"),
    [
        ("Numero di identificazione: AB1234567 in archivio.", "AB1234567", EntityType.NATIONAL_ID),
        ("Carta d'identità: CA12345AA verificata.", "CA12345AA", EntityType.NATIONAL_ID),
        ("CAP: 20144 Milano.", "20144", EntityType.LOCATION),
        ("Numero de identificación: 12345678Z registrado.", "12345678Z", EntityType.NATIONAL_ID),
        ("Código postal: 28001 Madrid.", "28001", EntityType.LOCATION),
        ("Ausweisnummer: T22000129 gültig bis 2030.", "T22000129", EntityType.NATIONAL_ID),
        ("Postleitzahl: 80331 München.", "80331", EntityType.LOCATION),
        ("Numéro de passeport: 12AB34567 valide.", "12AB34567", EntityType.NATIONAL_ID),
        ("Code postal: 75001 Paris.", "75001", EntityType.LOCATION),
        ("Căn cước công dân 012345678901 cấp tại Hà Nội.", "012345678901", EntityType.NATIONAL_ID),
        ("Số hộ chiếu B1234567 có hiệu lực.", "B1234567", EntityType.NATIONAL_ID),
        ("Nomor KTP: 3171012345678901 aktif.", "3171012345678901", EntityType.NATIONAL_ID),
        ("Nomor SIM: 123456789012 resmi.", "123456789012", EntityType.NATIONAL_ID),
        ("居民身份证 110101199003072345 登记有效。", "110101199003072345", EntityType.NATIONAL_ID),
        ("纳税人识别号 91110108MA0012345 已认证。", "91110108MA0012345", EntityType.TAX_ID),
    ],
)
def test_multilingual_context_rules(text: str, value: str, entity_type: EntityType) -> None:
    detections = ContextualIdDetector().detect(text)
    assert [(text[item.start : item.end], item.entity_type) for item in detections] == [
        (value, entity_type)
    ]


@pytest.mark.parametrize(
    "text",
    [
        "Running software version 2.4.1 in production.",
        "System build version v1.0.4 passed all integration tests.",
        "Server returned HTTP status code 200 OK.",
        "Listening on port 8080 for incoming connections.",
        "Reference page 100200 in the system administrator manual.",
        "See line 123456 for the syntax error location.",
        "Commit revision 8ec7e11 was merged to main branch.",
    ],
)
def test_negative_context_suppresses_false_positives(text: str) -> None:
    assert ContextualIdDetector().detect(text) == []


def test_explainable_bounded_scoring() -> None:
    # A candidate with an immediate separator (colon) scores higher than distant separated tokens
    close_detection = ContextualIdDetector().detect("Passport No: X1234567")[0]
    distant_detection = ContextualIdDetector().detect(
        "Passport No identified as under the number of X1234567"
    )[0]

    assert 0.75 <= close_detection.confidence <= 1.0
    assert 0.75 <= distant_detection.confidence <= 1.0
    assert close_detection.confidence > distant_detection.confidence
