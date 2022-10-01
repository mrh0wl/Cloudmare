"""Base for interacting with the Censys APIs."""
import json
import os
import warnings
from functools import wraps
from typing import Any, Callable, Optional, Type

import backoff
import thirdparty.requests as requests
from thirdparty.requests.models import Response

from .exceptions import (
    CensysAPIException,
    CensysException,
    CensysJSONDecodeException,
    CensysTooManyRequestsException,
)
from .version import __version__


# Wrapper to make max_retries configurable at runtime
def _backoff_wrapper(method: Callable):
    @wraps(method)
    def _wrapper(self, *args, **kwargs):
        @backoff.on_exception(
            backoff.expo,
            (
                CensysTooManyRequestsException,
                requests.exceptions.Timeout,
            ),
            max_tries=self.max_retries,
            max_time=self.timeout,
        )
        def _impl():
            return method(self, *args, *kwargs)

        return _impl()

    return _wrapper


class CensysAPIBase:
    """This is the base class for API queries."""

    DEFAULT_TIMEOUT: int = 30
    """Default API timeout."""
    DEFAULT_USER_AGENT: str = f"censys/{__version__}"
    """Default API user agent."""
    DEFAULT_MAX_RETRIES: int = 5
    """Default max number of API retries."""

    def __init__(
        self,
        url: Optional[str] = None,
        timeout: Optional[int] = DEFAULT_TIMEOUT,
        max_retries: Optional[int] = DEFAULT_MAX_RETRIES,
        user_agent: Optional[str] = DEFAULT_USER_AGENT,
        proxies: Optional[dict] = None,
        cookies: Optional[dict] = None,
        **kwargs,
    ):
        """Inits CensysAPIBase.

        Args:
            url (str): Optional; The URL to make API requests.
            timeout (int): Optional; Timeout for API requests in seconds.
            max_retries (int):
                Optional; Max number of times to retry failed API requests.
            user_agent (str): Optional; Override User-Agent string.
            proxies (dict): Optional; Configure HTTP proxies.
            cookies (dict): Optional; Configure cookies.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            CensysException: Base Exception Class for the Censys API.
        """
        # Get common request settings
        self.timeout = timeout
        self.max_retries = max_retries
        self._api_url = url or os.getenv("CENSYS_API_URL")

        if not self._api_url:
            raise CensysException("No API url configured.")

        # Create a session and set credentials
        self._session = requests.Session()
        if proxies:
            if "http" in proxies:
                warnings.warn("HTTP proxies will not be used.")
                proxies.pop("http", None)
            self._session.proxies.update(proxies)
        if cookies:
            self._session.cookies.update(cookies)
        self._session.headers.update(
            {
                "accept": "application/json, */8",
                "User-Agent": " ".join(
                    [
                        requests.utils.default_user_agent(),
                        user_agent
                        or kwargs.get("user_agent_identifier")
                        or self.DEFAULT_USER_AGENT,
                    ]
                ),
            }
        )

    @staticmethod
    def _get_exception_class(_: Response) -> Type[CensysAPIException]:
        """Maps HTTP status code or ASM error code to exception.

        Must be implemented by child class.

        Args:
            _ (Response): HTTP requests response object.

        Returns:
            Type[CensysAPIException]: Exception to raise.
        """
        return CensysAPIException

    @_backoff_wrapper
    def _make_call(
        self,
        method: Callable[..., Response],
        endpoint: str,
        args: Optional[dict] = None,
        data: Optional[Any] = None,
    ) -> dict:
        """Make API call.

        Wrapper functions for all our REST API calls checking for errors
        and decoding the responses.

        Args:
            method (Callable): Method to send HTTP request.
            endpoint (str): The path of API endpoint.
            args (dict): Optional; URL args that are mapped to params.
            data (Any): Optional; JSON data to serialize with request.

        Raises:
            censys_exception: Exception Class for the Censys API.
            CensysJSONDecodeException: Exception for decoding JSON.

        Returns:
            dict: Results from an API request.
        """
        if endpoint.startswith("/"):
            url = f"{self._api_url}{endpoint}"
        else:
            url = f"{self._api_url}/{endpoint}"

        request_kwargs = {
            "params": args or {},
            "timeout": self.timeout,
        }

        if data:
            request_kwargs["json"] = data

        res = method(url, **request_kwargs)

        if res.status_code in range(200, 300):
            # Check for a returned json body
            try:
                json_data = res.json()
                if "error" not in json_data:
                    return json_data
            # Successful request returned no json body in response
            except ValueError:
                return {
                    "code": res.status_code,
                    "status": res.reason,
                }

        try:
            json_data = res.json()
            message = json_data.get("error") or json_data.get("message")
            const = json_data.get("error_type") or json_data.get("status") or "unknown"
            error_code = json_data.get("errorCode", "unknown")
            details = json_data.get("details", "unknown")
        except (ValueError, json.decoder.JSONDecodeError) as error:
            message = (
                f"Response from {res.url} is not valid JSON and cannot be decoded."
            )
            raise CensysJSONDecodeException(
                status_code=res.status_code,
                message=message,
                body=res.text,
                const="badjson",
            ) from error

        censys_exception = self._get_exception_class(res)
        raise censys_exception(
            status_code=res.status_code,
            body=res.text,
            const=const,
            message=message,
            error_code=error_code,
            details=details,
        )

    def _get(self, endpoint: str, args: Optional[dict] = None) -> dict:
        return self._make_call(self._session.get, endpoint, args)

    def _post(
        self, endpoint: str, args: Optional[dict] = None, data: Optional[dict] = None
    ) -> dict:
        return self._make_call(self._session.post, endpoint, args, data)

    def _put(
        self, endpoint: str, args: Optional[dict] = None, data: Optional[dict] = None
    ) -> dict:
        return self._make_call(self._session.put, endpoint, args, data)

    def _delete(self, endpoint: str, args: Optional[dict] = None) -> dict:
        return self._make_call(self._session.delete, endpoint, args)
