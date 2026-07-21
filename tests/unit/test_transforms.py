import re

import pytest

from pseudonymize import Detection, EntityType, generate_key
from pseudonymize.exceptions import InvalidKeyError
from pseudonymize.transforms import HmacTransformer, RedactTransformer


def detection(entity_type: EntityType = EntityType.EMAIL) -> Detection:
    return Detection(entity_type, 0, 17, 1.0, "test")


def test_hmac_is_deterministic_and_domain_separated() -> None:
    key = b"k" * 32
    first = HmacTransformer(key, "a").transform("Maria@EXAMPLE.com", detection())
    assert first == HmacTransformer(key, "a").transform("Maria@example.com", detection())
    assert first != HmacTransformer(key, "b").transform("Maria@example.com", detection())
    assert re.fullmatch(r"<PZ1:EMAIL:[A-Z2-7]{16}>", first)


def test_normalization_for_structured_types() -> None:
    transformer = HmacTransformer(b"k" * 32)
    iban = detection(EntityType.IBAN)
    card = detection(EntityType.PAYMENT_CARD)
    phone = detection(EntityType.PHONE)
    ip = detection(EntityType.IP_ADDRESS)
    assert transformer.transform("GB82 WEST 1234", iban) == transformer.transform(
        "gb82west1234", iban
    )
    assert transformer.transform("4111-1111", card) == transformer.transform("41111111", card)
    assert transformer.transform("+39 333", phone) == transformer.transform("+39333", phone)
    assert transformer.transform("2001:0db8::1", ip) == transformer.transform("2001:db8::1", ip)
    secret = detection(EntityType.SECRET)
    assert transformer.transform(" token ", secret) == transformer.transform("token", secret)


def test_key_validation_generation_and_redaction() -> None:
    with pytest.raises(InvalidKeyError):
        HmacTransformer(b"short")
    with pytest.raises(ValueError, match="namespace"):
        HmacTransformer(b"k" * 32, "invalid\0namespace")
    assert len(generate_key()) == 32
    assert RedactTransformer().transform("anything", detection()) == "<EMAIL>"
