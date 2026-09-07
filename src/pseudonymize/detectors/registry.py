from pseudonymize.detectors.base import Detector
from pseudonymize.detectors.checksums import AlgorithmicChecksumDetector
from pseudonymize.detectors.context import ContextualIdDetector
from pseudonymize.detectors.email import EmailDetector
from pseudonymize.detectors.iban import IbanDetector
from pseudonymize.detectors.ip_address import IpAddressDetector
from pseudonymize.detectors.italian import ItalianFiscalCodeDetector, ItalianVATDetector
from pseudonymize.detectors.location import LocationDetector
from pseudonymize.detectors.organization import OrganizationDetector
from pseudonymize.detectors.payment_card import PaymentCardDetector
from pseudonymize.detectors.phone import PhoneDetector
from pseudonymize.detectors.secret import SecretDetector
from pseudonymize.detectors.url import UrlDetector

DEFAULT_DETECTORS: tuple[Detector, ...] = (
    EmailDetector(),
    IpAddressDetector(),
    PaymentCardDetector(),
    IbanDetector(),
    ItalianFiscalCodeDetector(),
    ItalianVATDetector(),
    ContextualIdDetector(),
    AlgorithmicChecksumDetector(),
    PhoneDetector(),
    UrlDetector(),
    SecretDetector(),
    LocationDetector(),
    OrganizationDetector(),
)
