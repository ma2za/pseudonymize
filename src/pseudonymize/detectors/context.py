import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_HAS_DIGIT = re.compile(r"\d")

# Tokenizer pattern for finding words or contiguous alphanumeric blocks
_TOKEN_PATTERN = re.compile(r"[A-Z0-9-]+|[^\w\s]", re.IGNORECASE)

# Words and punctuation safely ignored when linking a context label to its value
_DEPENDENCY_LINKS = frozenset(
    {
        "is",
        "are",
        "was",
        "were",
        "of",
        "for",
        "the",
        "a",
        "an",
        "number",
        "no",
        "id",
        "ending",
        "in",
        "with",
        "exactly",
        ":",
        "-",
        "#",
        "(",
        ")",
        ".",
        ",",
        "[",
        "]",
        "{",
        "}",
        "as",
        "under",
        "identified",
        "by",
        "like",
        "bearing",
    }
)

_CONTEXT_RULES = [
    # National identity documents
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:identification\s*number|identity\s*(?:card|number)"
            r"|id\s*card|national\s*id|registration\s*number"
            r"|numéro\s*d'identification|número\s*de\s*identificación"
            r"|chứng\s*minh\s*nhân\s*dân|căn\s*cước|身份证号"
            r"|passport\s*(?:no\.?|number|#)?|护照号|paspor"
            r"|driver'?s?\s*licen[sc]e|driving\s*licen[sc]e|nomor\s*SIM|số\s*giấy\s*phép\s*lái\s*xe"
            r"|dni|ktp|nik|rg|ine|nric|hkid"
            r"|(?:ticket|receipt|serial|reference|ref|case|customer|user|member|employee'?s?)\s*(?:id|no\.?|number|#|identifier|:))(?![a-z0-9_])"
        ),
        EntityType.NATIONAL_ID,
        re.compile(r"^[A-Z0-9-]{6,20}$", re.IGNORECASE),
    ),
    # Tax identifiers
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:tax\s*(?:no\.?|number|reference|identifier|id|record)|tin"
            r"|vat\s*(?:no\.?|number|id)|mã\s*số\s*thuế|nomor\s*pajak|税号"
            r"|rfc|nit|rut|siren|siret)(?![a-z0-9_])"
        ),
        EntityType.TAX_ID,
        re.compile(r"^[A-Z0-9-]{6,20}$", re.IGNORECASE),
    ),
    # Postal codes
    (
        re.compile(r"(?i)(?<![a-z0-9_])(?:zip\s*code|postal\s*code|postcode|zip|cap)(?![a-z0-9_])"),
        EntityType.LOCATION,
        re.compile(r"^[0-9]{5,6}$"),
    ),
    # Account, policy, and insurance numbers
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:account|policy|insurance)\s*(?:no\.?|number|#)(?![a-z0-9_])"
        ),
        EntityType.SECRET,
        re.compile(r"^[A-Z0-9-]{6,16}$", re.IGNORECASE),
    ),
    # Payment cards
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:credit\s*card|debit\s*card|card\s*number|visa|mastercard"
            r"|maestro|amex)(?![a-z0-9_])"
        ),
        EntityType.PAYMENT_CARD,
        re.compile(r"^[\d-]{13,24}$"),
    ),
]


@dataclass(frozen=True, slots=True)
class ContextualIdDetector:
    name: str = "context_id"

    def detect(self, text: str) -> list[Detection]:
        detections = []
        for trigger_regex, entity_type, value_regex in _CONTEXT_RULES:
            for match in trigger_regex.finditer(text):
                start_search = match.end()

                # Scan a reasonable token window forward to find the dependent value
                window = text[start_search : start_search + 60]

                for token_match in _TOKEN_PATTERN.finditer(window):
                    token = token_match.group()

                    if token.lower() in _DEPENDENCY_LINKS:
                        continue

                    # Also skip consecutive punctuation strings
                    if not any(c.isalnum() for c in token):
                        continue

                    # Evaluate the first significant candidate token
                    if _HAS_DIGIT.search(token) and value_regex.match(token):
                        if entity_type is EntityType.PAYMENT_CARD:
                            stripped_len = len("".join(c for c in token if c.isdigit()))
                            if not (13 <= stripped_len <= 19):
                                break

                        actual_start = start_search + token_match.start()
                        actual_end = start_search + token_match.end()

                        detections.append(
                            Detection(entity_type, actual_start, actual_end, 0.90, self.name)
                        )

                    # Once we hit a significant token that is NOT a match or a stop word,
                    # the dependency chain is broken. Stop searching forward.
                    break

        return detections
