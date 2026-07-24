class PseudonymizeError(Exception):
    pass


class InvalidKeyError(PseudonymizeError, ValueError):
    pass


class UnsupportedDataError(PseudonymizeError, TypeError):
    pass


class AdapterContractError(PseudonymizeError, TypeError):
    pass


class AdapterExecutionError(PseudonymizeError, RuntimeError):
    pass


class FileProcessingError(PseudonymizeError, OSError):
    pass


class UnsupportedFormatError(PseudonymizeError, ValueError):
    pass


class BackendContractError(PseudonymizeError, TypeError):
    pass


class BackendExecutionError(PseudonymizeError, RuntimeError):
    pass


class NetworkPolicyError(PseudonymizeError, PermissionError):
    pass


class InvalidDetectionError(PseudonymizeError, ValueError):
    pass
