from pseudonymize.detectors.base import Detector
from pseudonymize.detectors.email import EmailDetector
from pseudonymize.detectors.iban import IbanDetector
from pseudonymize.detectors.ip_address import IpAddressDetector
from pseudonymize.detectors.payment_card import PaymentCardDetector
from pseudonymize.detectors.phone import PhoneDetector
from pseudonymize.detectors.secret import SecretDetector
from pseudonymize.detectors.url import UrlDetector

DEFAULT_DETECTORS: tuple[Detector, ...] = (
    EmailDetector(),
    IpAddressDetector(),
    PaymentCardDetector(),
    IbanDetector(),
    PhoneDetector(),
    UrlDetector(),
    SecretDetector(),
)
