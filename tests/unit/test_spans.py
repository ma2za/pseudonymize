from pseudonymize import Detection, EntityType
from pseudonymize.spans import resolve_overlaps


def test_overlap_prefers_validated_entity_then_stable_order() -> None:
    phone = Detection(EntityType.PHONE, 0, 19, 0.99, "phone")
    card = Detection(EntityType.PAYMENT_CARD, 0, 19, 1.0, "card")
    email = Detection(EntityType.EMAIL, 30, 40, 0.9, "email")
    assert resolve_overlaps([phone, email, card]) == (card, email)


def test_url_credential_outranks_overlapping_email() -> None:
    # In "https://alice:s3cret@host.example" the password plus host also match
    # the email pattern; the credential span must win or "alice:" leaks.
    credential = Detection(EntityType.URL_CREDENTIAL, 8, 20, 1.0, "url")
    email = Detection(EntityType.EMAIL, 14, 32, 0.99, "email")
    assert resolve_overlaps([email, credential]) == (credential,)


def test_configured_priority_breaks_equal_rank() -> None:
    first = Detection(EntityType.SECRET, 0, 10, 0.9, "first")
    second = Detection(EntityType.SECRET, 5, 15, 0.9, "second")
    assert resolve_overlaps([first, second], ("second", "first")) == (second,)
