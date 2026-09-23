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

# Negative context keywords indicating non-personal reference values (versions, ports, pages)
_NEGATIVE_CONTEXT = re.compile(
    r"(?i)\b(?:version|v\d|release|build|commit|revision|rev|port|page|p\.|line|status\s*code|http\s*(?:status)?)\b"
)

# Software version-like pattern (e.g. 1.2.3, 2.0.1, v1.0.0)
_VERSION_LIKE = re.compile(r"^v?\d+(?:\.\d+)+(?:-[a-z0-9]+)?$", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class ContextRule:
    """Locale-scoped, data-driven contextual identification rule."""

    name: str
    languages: tuple[str, ...]
    entity_type: EntityType
    trigger_regex: re.Pattern[str]
    value_regex: re.Pattern[str]
    window_length: int = 60
    base_confidence: float = 0.88
    rationale: str = ""


_CONTEXT_RULES: tuple[ContextRule, ...] = (
    # National identity documents across multiple locales
    ContextRule(
        name="national_id_context",
        languages=("en", "es", "fr", "it", "de", "vi", "id", "zh"),
        entity_type=EntityType.NATIONAL_ID,
        trigger_regex=re.compile(
            r"(?i)(?<![a-z0-9_])(?:"
            r"identification\s*number|identity\s*(?:card|number)"
            r"|id\s*card|national\s*id|registration\s*number"
            r"|n[uú]mero\s*(?:d['e]|di)\s*identifica[cz]i[oó]n(?:e)?"
            r"|carte\s*d'identité|carta\s*d'identità|ausweisnummer|personalausweisnummer"
            r"|chứng\s*minh\s*nhân\s*dân|căn\s*cước(?:\s*công\s*dân)?|身份证号|居民身份证"
            r"|passport\s*(?:no\.?|number|#)?|numéro\s*de\s*passeport|passnummer|护照号|paspor|số\s*hộ\s*chiếu"
            r"|driver'?s?\s*licen[sc]e|driving\s*licen[sc]e|nomor\s*SIM|số\s*giấy\s*phép\s*lái\s*xe"
            r"|dni|ktp|nik|rg|ine|nric|hkid"
            r"|(?:ticket|receipt|serial|reference|ref|case|customer|user|member|employee'?s?)\s*(?:id|no\.?|number|#|identifier|:)"
            r")(?![a-z0-9_])"
        ),
        value_regex=re.compile(r"^[A-Z0-9-]{6,20}$", re.IGNORECASE),
        window_length=60,
        base_confidence=0.88,
        rationale=(
            "Matches national identity, passport, license, and official ID labels "
            "followed by alphanumeric tokens."
        ),
    ),
    # Tax and VAT identifiers across multiple locales
    ContextRule(
        name="tax_id_context",
        languages=("en", "es", "fr", "it", "de", "vi", "id", "zh"),
        entity_type=EntityType.TAX_ID,
        trigger_regex=re.compile(
            r"(?i)(?<![a-z0-9_])(?:"
            r"tax\s*(?:no\.?|number|reference|identifier|id|record)|tin"
            r"|vat\s*(?:no\.?|number|id)|numéro\s*(?:fiscal|de\s*tva)|mã\s*số\s*thuế|nomor\s*pajak|税号|纳税人识别号"
            r"|steuernummer|steuer-id|steuer-identifikationsnummer|ust-idnr|npwp"
            r"|rfc|nit|rut|cif|siren|siret"
            r")(?![a-z0-9_])"
        ),
        value_regex=re.compile(r"^[A-Z0-9-]{6,20}$", re.IGNORECASE),
        window_length=60,
        base_confidence=0.88,
        rationale=(
            "Matches tax, VAT, and fiscal registry headers followed by registered "
            "business or personal tax tokens."
        ),
    ),
    # Postal codes (location context)
    ContextRule(
        name="postal_code_context",
        languages=("en", "it", "es", "fr", "de"),
        entity_type=EntityType.LOCATION,
        trigger_regex=re.compile(
            r"(?i)(?<![a-z0-9_])(?:"
            r"zip\s*code|postal\s*code|postcode|zip|cap|código\s*postal|code\s*postal|postleitzahl|plz"
            r")(?![a-z0-9_])"
        ),
        value_regex=re.compile(r"^[0-9]{4,6}$"),
        window_length=40,
        base_confidence=0.88,
        rationale="Matches numeric postal codes preceded by unambiguous postal code indicators.",
    ),
    # Account, policy, and secret reference numbers
    ContextRule(
        name="account_policy_context",
        languages=("en", "es", "fr", "de", "it"),
        entity_type=EntityType.SECRET,
        trigger_regex=re.compile(
            r"(?i)(?<![a-z0-9_])(?:"
            r"(?:account|policy|insurance)\s*(?:no\.?|number|#)"
            r"|numéro\s*de\s*(?:compte|police)|número\s*de\s*(?:cuenta|póliza)|numero\s*di\s*(?:conto|polizza)"
            r"|kontonummer|versicherungsnummer|policennummer"
            r")(?![a-z0-9_])"
        ),
        value_regex=re.compile(r"^[A-Z0-9-]{6,16}$", re.IGNORECASE),
        window_length=50,
        base_confidence=0.88,
        rationale=(
            "Matches financial account, policy, or insurance reference numbers "
            "under clear label headers."
        ),
    ),
    # Payment cards under context triggers
    ContextRule(
        name="payment_card_context",
        languages=("en", "es", "fr", "de", "it"),
        entity_type=EntityType.PAYMENT_CARD,
        trigger_regex=re.compile(
            r"(?i)(?<![a-z0-9_])(?:"
            r"credit\s*card|debit\s*card|card\s*number|tarjeta\s*de\s*(?:crédito|débito)|carte\s*de\s*crédit|carta\s*di\s*credito|kreditkarte"
            r"|visa|mastercard|maestro|amex"
            r")(?![a-z0-9_])"
        ),
        value_regex=re.compile(r"^[\d-]{13,24}$"),
        window_length=50,
        base_confidence=0.88,
        rationale="Matches credit and debit card numbers following payment card indicators.",
    ),
)


def _calculate_score(
    rule: ContextRule,
    distance: int,
    has_separator: bool,
    has_negative_context: bool,
) -> float:
    """Calculate an explainable bounded confidence score for a contextual candidate.

    Scores decay gently with token distance from the trigger label, receive a boost
    for explicit separators (e.g. colons or hashes), and are heavily penalized if
    negative context indicators (e.g. versions, ports, pages) occur in the window.
    """
    score = rule.base_confidence

    # Distance penalty: linear decay up to 0.08 across the window length
    distance_fraction = min(1.0, distance / max(1, rule.window_length))
    score -= distance_fraction * 0.08

    # Explicit separator boost (+0.04)
    if has_separator:
        score += 0.04

    # Negative context penalty (-0.30)
    if has_negative_context:
        score -= 0.30

    return max(0.0, min(1.0, round(score, 3)))


@dataclass(frozen=True, slots=True)
class ContextualIdDetector:
    name: str = "context_id"

    def detect(self, text: str) -> list[Detection]:
        detections = []
        for rule in _CONTEXT_RULES:
            for match in rule.trigger_regex.finditer(text):
                start_search = match.end()

                # Scan forward within the rule's defined window length
                window = text[start_search : start_search + rule.window_length]

                has_separator = False
                has_negative = bool(_NEGATIVE_CONTEXT.search(window))

                for token_match in _TOKEN_PATTERN.finditer(window):
                    token = token_match.group()

                    if token in (":", "#", "="):
                        has_separator = True

                    if token.lower() in _DEPENDENCY_LINKS:
                        continue

                    # Skip non-alphanumeric punctuation clusters
                    if not any(c.isalnum() for c in token):
                        continue

                    # Filter out version-like numbers (e.g. 1.2.3)
                    if _VERSION_LIKE.match(token):
                        break

                    # Evaluate candidate token against value criteria
                    if _HAS_DIGIT.search(token) and rule.value_regex.match(token):
                        if rule.entity_type is EntityType.PAYMENT_CARD:
                            stripped_len = len("".join(c for c in token if c.isdigit()))
                            if not (13 <= stripped_len <= 19):
                                break

                        distance = token_match.start()
                        score = _calculate_score(rule, distance, has_separator, has_negative)

                        # Enforce bounded threshold for emission
                        if score >= 0.75:
                            actual_start = start_search + token_match.start()
                            actual_end = start_search + token_match.end()

                            detections.append(
                                Detection(
                                    rule.entity_type,
                                    actual_start,
                                    actual_end,
                                    score,
                                    self.name,
                                )
                            )

                    # Once we hit a significant token that is evaluated, stop searching forward
                    break

        return detections
