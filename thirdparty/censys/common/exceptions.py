"""Exceptions for Censys."""
from typing import Dict, Optional, Type


class CensysException(Exception):
    """Base Exception for Censys."""


class CensysCLIException(CensysException):
    """Exception raised when the CLI is passed invalid arguments."""


class CensysAPIException(CensysException):
    """Base Exception for Censys APIs."""

    def __init__(
        self,
        status_code: int,
        message: str,
        body: Optional[str] = None,
        const: Optional[str] = None,
        error_code: Optional[int] = None,
        details: Optional[str] = None,
    ):
        """Inits CensysAPIException.

        Args:
            status_code (int): HTTP status code.
            message (str): HTTP message.
            body (str): Optional; HTTP body.
            const (str): Optional; Constant for manual errors.
            error_code (int): Optional; Error code.
            details (str): Optional; Additional details.
        """
        self.status_code = status_code
        self.message = message
        self.body = body
        self.const = const
        self.error_code = error_code
        self.details = details
        super().__init__(self.message)


class CensysSearchException(CensysAPIException):
    """Base Exception for the Censys search API."""

    def __repr__(self) -> str:
        """Representation of CensysSearchException.

        Returns:
            str: Printable representation.
        """
        return f"{self.status_code} ({self.const}): {self.message or self.body}"

    __str__ = __repr__


class CensysAsmException(CensysAPIException):
    """Base Exception for the Censys ASM API."""

    def __repr__(self) -> str:
        """Representation of CensysAsmException.

        Returns:
            str: Printable representation.
        """
        return (
            f"{self.status_code} (Error Code: {self.error_code}), "
            f"{self.message}. {self.details}"
        )

    __str__ = __repr__


class CensysMissingApiKeyException(CensysAsmException):
    """Exception raised when there is no provided ASM API key."""


class CensysRateLimitExceededException(CensysSearchException):
    """Exception raised when your Censys rate limit has been exceeded."""


class CensysNotFoundException(CensysSearchException):
    """Exception raised when the resource requested is not found."""


class CensysUnauthorizedException(CensysSearchException):
    """Exception raised when you doesn't have access to the requested resource."""


class CensysJSONDecodeException(CensysSearchException):
    """Exception raised when the resource requested is not valid JSON."""


class CensysInvalidRequestException(CensysAsmException):
    """Exception raised when the HTTP request is invalid."""


class CensysInvalidAuthTokenException(CensysAsmException):
    """Exception raised when the auth token is invalid."""


class CensysInvalidAPIKeyException(CensysAsmException):
    """Exception raised when the ASM API key is invalid."""


class CensysTooManyRequestsException(CensysAsmException):
    """Exception raised when the allowed requests bandwidth is exceeded."""


class CensysAppDownForMaintenanceException(CensysAsmException):
    """Exception raised when the ASM API is down for maintenance."""


class CensysInvalidSeedDataException(CensysAsmException):
    """Exception raised when the seed data is invalid."""


class CensysAssociatedAssetsThresholdWarningException(CensysAsmException):
    """Exception raised when the asset count is within the warning threshold."""


class CensysTooManyInputNodesException(CensysAsmException):
    """Exception raised when there are too many input nodes."""


class CensysSeedNotFoundException(CensysAsmException):
    """Exception raised when the requested seed can not be found."""


class CensysNotASeedException(CensysAsmException):
    """Exception raised when the requested resource is not a seed."""


class CensysNeedConfirmationToRemoveParentSeedsException(CensysAsmException):
    """Exception raised when confirmation is needed to remove seeds with children."""


class CensysCannotRemoveNonExistentSeedsException(CensysAsmException):
    """Exception raised when trying to remove non existent seed nodes."""


class CensysCannotRemoveNonSeedsException(CensysAsmException):
    """Exception raised when trying to remove non seed nodes."""


class CensysInvalidSeedTypeException(CensysAsmException):
    """Exception raised when the seed type is invalid."""


class CensysInvalidLogbookCursorException(CensysAsmException):
    """Exception raised when the logbook cursor is invalid."""


class CensysPageNumberOutOfRangeException(CensysAsmException):
    """Exception raised when the page number is out of range [1 - totalPages]."""


class CensysInvalidPageSizeException(CensysAsmException):
    """Exception raised when the page size is invalid."""


class CensysHostNotFoundException(CensysAsmException):
    """Exception raised when the requested host is not found."""


class CensysInvalidIPv4AddressException(CensysAsmException):
    """Exception raised when the IPv4 address is invalid."""


class CensysInvalidCommentException(CensysAsmException):
    """Exception raised when the comment is invalid."""


class CensysCommentNotFoundException(CensysAsmException):
    """Exception raised when the requested comment is not found."""


class CensysInvalidColorException(CensysAsmException):
    """Exception raised when the specified color is invalid."""


class CensysTagHasTrailingOrLeadingWhitespaceException(CensysAsmException):
    """Exception raised when the specified tag has trailing or leading whitespace."""


class CensysTagIsEmptyStringException(CensysAsmException):
    """Exception raised when the specified tag is an empty string."""


class CensysTagLabelsDifferOnlyInCasingException(CensysAsmException):
    """Exception raised when the tag differs from an existing tag in only casing."""


class CensysTagLabelTooLongException(CensysAsmException):
    """Exception raised when the specified tag label is too long."""


class CensysTagColorTooLongException(CensysAsmException):
    """Exception raised when the specified tag color is too long."""


class CensysCannotCreateTagWithNewColorException(CensysAsmException):
    """Exception raised when the specified tag cannot be created with a new color."""


class CensysTagColorHasTrailingOrLeadingWhitespaceException(CensysAsmException):
    """Exception raised when the tag color has trailing or leading whitespace."""


class CensysCertificateNotFoundException(CensysAsmException):
    """Exception raised when the certificate is not found."""


class CensysDomainNotFoundException(CensysAsmException):
    """Exception raised when the domain is not found."""


class CensysInvalidCloudAssetDataException(CensysAsmException):
    """Exception raised when invalid cloud asset data is submitted."""


class CensysInvalidObjectStorageAssetIdentifierException(CensysAsmException):
    """Exception raised when object storage name is not a valid asset URL."""


class CensysInvalidObjectStorageAssetNotFoundException(CensysAsmException):
    """Exception raised when no object storage assets with given URL were found."""


class CensysBadJSONBodyException(CensysAsmException):
    """Exception raised when a bad JSON string is in the body."""


class CensysRiskNotFoundException(CensysAsmException):
    """Exception raised when no risks are found with given risk_id."""


class CensysInvalidDateException(CensysAsmException):
    """Exception raised when an invalid date is submitted."""


class CensysInvalidCloudException(CensysAsmException):
    """Exception raised when an invalid cloud is submitted."""


class CensysExceptionMapper:
    """Map status code to Exception for the ASM and Search API."""

    ASM_EXCEPTIONS: Dict[int, Type[CensysAsmException]] = {
        10000: CensysMissingApiKeyException,
        10001: CensysInvalidAPIKeyException,
        10002: CensysInvalidAuthTokenException,
        10007: CensysInvalidSeedDataException,
        10008: CensysInvalidRequestException,
        10011: CensysCannotRemoveNonSeedsException,
        10012: CensysCannotRemoveNonExistentSeedsException,
        10013: CensysNeedConfirmationToRemoveParentSeedsException,
        10014: CensysSeedNotFoundException,
        10015: CensysNotASeedException,
        10016: CensysTooManyInputNodesException,
        10017: CensysAssociatedAssetsThresholdWarningException,
        10018: CensysHostNotFoundException,
        10019: CensysDomainNotFoundException,
        10020: CensysCertificateNotFoundException,
        10021: CensysInvalidIPv4AddressException,
        10025: CensysTagHasTrailingOrLeadingWhitespaceException,
        10026: CensysTagIsEmptyStringException,
        10027: CensysTagLabelsDifferOnlyInCasingException,
        10028: CensysTagLabelTooLongException,
        10029: CensysAppDownForMaintenanceException,
        10034: CensysTagColorTooLongException,
        10035: CensysCannotCreateTagWithNewColorException,
        10036: CensysTagColorHasTrailingOrLeadingWhitespaceException,
        10037: CensysInvalidColorException,
        10038: CensysInvalidSeedTypeException,
        10039: CensysTooManyRequestsException,
        10040: CensysInvalidLogbookCursorException,
        10050: CensysInvalidPageSizeException,
        10051: CensysPageNumberOutOfRangeException,
        10054: CensysInvalidCommentException,
        10055: CensysCommentNotFoundException,
        10059: CensysInvalidCloudAssetDataException,
        10060: CensysInvalidObjectStorageAssetIdentifierException,
        10061: CensysInvalidObjectStorageAssetNotFoundException,
        10067: CensysBadJSONBodyException,
        10073: CensysRiskNotFoundException,
        10078: CensysInvalidDateException,
        10082: CensysInvalidCloudException,
    }
    """Map of status code to ASM Exception."""

    SEARCH_EXCEPTIONS: Dict[int, Type[CensysSearchException]] = {
        401: CensysUnauthorizedException,
        403: CensysUnauthorizedException,
        404: CensysNotFoundException,
        429: CensysRateLimitExceededException,
    }
    """Map of status code to Search Exception."""
