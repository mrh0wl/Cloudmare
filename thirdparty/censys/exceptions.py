"""
Exceptions for Censys.
"""

from typing import Optional


class CensysException(Exception):
    """
    Base Exception for Censys.
    """


class CensysCLIException(CensysException):
    """
    Exception raised when the CLI is passed invalid arguments.
    """


class CensysAPIException(CensysException):
    """
    Base Exception for the Censys API.
    """

    def __init__(
        self,
        status_code: int,
        message: str,
        body: Optional[str] = None,
        const: Optional[str] = None,
    ):
        self.status_code = status_code
        self.message = message
        self.body = body
        self.const = const
        super().__init__(self.message)

    def __repr__(self):
        return "%i (%s): %s" % (self.status_code, self.const, self.message or self.body)

    __str__ = __repr__


class CensysRateLimitExceededException(CensysAPIException):
    """
    Exception raised when your Censys rate limit has been exceeded.
    """


class CensysNotFoundException(CensysAPIException):
    """
    Exception raised when the resource requested is not found.
    """


class CensysUnauthorizedException(CensysAPIException):
    """
    Exception raised when your Censys account doesn't have
    access to the requested resource.
    """


class CensysJSONDecodeException(CensysAPIException):
    """
    Exception raised when the resource requested is not valid JSON.
    """
