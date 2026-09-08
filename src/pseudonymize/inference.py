import re

from pseudonymize.document import ContentBlock, CSVCellLocation, Document
from pseudonymize.result import Detection, EntityType

COLUMN_SEMANTICS: dict[str, EntityType] = {
    "phone": EntityType.PHONE,
    "phone_number": EntityType.PHONE,
    "mobile": EntityType.PHONE,
    "mobile_number": EntityType.PHONE,
    "cell": EntityType.PHONE,
    "ssn": EntityType.NATIONAL_ID,
    "social_security": EntityType.NATIONAL_ID,
    "national_id": EntityType.NATIONAL_ID,
    "nino": EntityType.NATIONAL_ID,
    "cpf": EntityType.NATIONAL_ID,
    "email": EntityType.EMAIL,
    "email_address": EntityType.EMAIL,
    "card": EntityType.PAYMENT_CARD,
    "credit_card": EntityType.PAYMENT_CARD,
    "pan": EntityType.PAYMENT_CARD,
    "card_number": EntityType.PAYMENT_CARD,
    "iban": EntityType.IBAN,
    "account": EntityType.IBAN,
    "account_number": EntityType.IBAN,
    "ip": EntityType.IP_ADDRESS,
    "ip_address": EntityType.IP_ADDRESS,
    "password": EntityType.SECRET,
    "secret": EntityType.SECRET,
    "token": EntityType.SECRET,
    "tax_id": EntityType.TAX_ID,
    "vat": EntityType.TAX_ID,
    "tin": EntityType.TAX_ID,
    "fiscal_code": EntityType.TAX_ID,
    "name": EntityType.PERSON,
    "first_name": EntityType.PERSON,
    "last_name": EntityType.PERSON,
    "full_name": EntityType.PERSON,
    "person": EntityType.PERSON,
    "employee": EntityType.PERSON,
    "customer": EntityType.PERSON,
    "city": EntityType.LOCATION,
    "address": EntityType.LOCATION,
    "zip": EntityType.LOCATION,
    "zipcode": EntityType.LOCATION,
    "location": EntityType.LOCATION,
    "company": EntityType.ORGANIZATION,
    "organization": EntityType.ORGANIZATION,
    "org": EntityType.ORGANIZATION,
}


def _normalize_header(header: str) -> str:
    return re.sub(r"[^a-z0-9]", "_", header.strip().lower()).strip("_")


class TabularInferenceLayout:
    def __init__(self, document: Document) -> None:
        self.csv_semantics: dict[int, EntityType] = {}

        # Determine CSV layout
        for block in document.blocks:
            loc = block.location
            if isinstance(loc, CSVCellLocation) and loc.row == 0:
                norm = _normalize_header(block.text)
                if norm in COLUMN_SEMANTICS:
                    self.csv_semantics[loc.column] = COLUMN_SEMANTICS[norm]
            # Since blocks are ordered, we can stop early if we pass row 0, but no harm continuing

    def extract_csv_detections(self, block: ContentBlock) -> list[Detection]:
        loc = block.location
        if isinstance(loc, CSVCellLocation) and loc.row > 0 and loc.column in self.csv_semantics:
            entity_type = self.csv_semantics[loc.column]
            text = block.text.strip()
            if text:
                start = block.text.find(text)
                end = start + len(text)
                return [Detection(entity_type, start, end, 1.0, "tabular", "layout_pass")]
        return []
