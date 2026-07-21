class PseudonymizeError(Exception):
    pass


class InvalidKeyError(PseudonymizeError, ValueError):
    pass


class UnsupportedDataError(PseudonymizeError, TypeError):
    pass
