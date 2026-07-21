import ipaddress
import unicodedata

from pseudonymize.result import EntityType


def normalize(value: str, entity_type: EntityType) -> str:
    value = unicodedata.normalize("NFKC", value).strip()
    if entity_type is EntityType.EMAIL:
        local, separator, domain = value.rpartition("@")
        return f"{local}{separator}{domain.lower()}"
    if entity_type in {EntityType.IBAN, EntityType.PAYMENT_CARD, EntityType.PHONE}:
        prefix = "+" if entity_type is EntityType.PHONE and value.startswith("+") else ""
        compact = "".join(character for character in value if character.isdigit())
        if entity_type is EntityType.IBAN:
            return "".join(value.split()).upper()
        return prefix + compact
    if entity_type is EntityType.IP_ADDRESS:
        return ipaddress.ip_address(value.strip("[]")).compressed
    return value
