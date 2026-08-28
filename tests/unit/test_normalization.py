from pseudonymize import EntityType
from pseudonymize.normalization import normalize


def test_structured_values_normalize_to_stable_alias_inputs() -> None:
    assert normalize("+39 333 123 4567", EntityType.PHONE) == "+393331234567"
    assert normalize("333 123 4567", EntityType.PHONE) == "3331234567"
    assert normalize("gb82 west 1234 5698 7654 32", EntityType.IBAN) == ("GB82WEST12345698765432")
    assert normalize("4111-1111-1111-1111", EntityType.PAYMENT_CARD) == ("4111111111111111")
    assert normalize("[2001:0db8::1]", EntityType.IP_ADDRESS) == "2001:db8::1"
    assert normalize("tsttst90a01z999m", EntityType.NATIONAL_ID) == "TSTTST90A01Z999M"
    assert normalize("IT 12345678903", EntityType.TAX_ID) == "IT12345678903"
    assert normalize("  token value  ", EntityType.SECRET) == "token value"
