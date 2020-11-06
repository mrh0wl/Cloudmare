"""
Base for interacting with the Censys Search API.
"""
# pylint: disable=too-many-arguments

import os
import json
from typing import Type, Optional, Callable, Dict, List, Generator, Any

import thirdparty.requests

from thirdparty.censys import __name__ as NAME, __version__ as VERSION
from thirdparty.censys.config import get_config, DEFAULT
from thirdparty.censys.exceptions import (
    CensysException,
    CensysAPIException,
    CensysRateLimitExceededException,
    CensysNotFoundException,
    CensysUnauthorizedException,
    CensysJSONDecodeException,
)

Fields = Optional[List[str]]


class CensysAPIBase:
    """
    This class is the base for API queries.

    Args:
        api_id (str, optional): The API ID provided by Censys.
        api_secret (str, optional): The API secret provided by Censys.
        url (str, optional): The URL to make API thirdparty.requests.
        timeout (int, optional): Timeout for API thirdparty.requests in seconds.
        user_agent_identifier (str, optional): Override User-Agent string.

    Raises:
        CensysAPIException: Base Exception Class for the Censys API.
    """

    DEFAULT_URL: str = "https://censys.io/api/v1"
    """Default API base URL."""
    DEFAULT_TIMEOUT: int = 30
    """Default API timeout."""
    DEFAULT_USER_AGENT: str = "%s/%s" % (NAME, VERSION)
    """Default API user agent."""
    EXCEPTIONS: Dict[int, Type[CensysAPIException]] = {
        401: CensysUnauthorizedException,
        403: CensysUnauthorizedException,
        404: CensysNotFoundException,
        429: CensysRateLimitExceededException,
    }
    """Map of status code to Exception."""

    def __init__(
        self,
        api_id: Optional[str] = None,
        api_secret: Optional[str] = None,
        url: Optional[str] = None,
        timeout: Optional[int] = None,
        user_agent_identifier: Optional[str] = None,
    ):
        # Gets config file
        config = get_config()

        # Try to get credentials
        self.api_id = (
            api_id or os.getenv("CENSYS_API_ID") or config.get(DEFAULT, "api_id")
        )
        self.api_secret = (
            api_secret
            or os.getenv("CENSYS_API_SECRET")
            or config.get(DEFAULT, "api_secret")
        )
        if not self.api_id or not self.api_secret:
            raise CensysException("No API ID or API secret configured.")

        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self._api_url = url or os.getenv("CENSYS_API_URL") or self.DEFAULT_URL

        # Create a session and sets credentials
        self._session = thirdparty.requests.Session()
        self._session.auth = (self.api_id, self.api_secret)
        self._session.headers.update(
            {
                "accept": "application/json, */8",
                "User-Agent": " ".join(
                    [
                        thirdparty.requests.utils.default_user_agent(),
                        user_agent_identifier or self.DEFAULT_USER_AGENT,
                    ]
                ),
            }
        )

        # Confirm setup
        self.account()

    def _get_exception_class(self, status_code: int) -> Type[CensysAPIException]:
        """Maps HTTP status code to exception.

        Args:
            status_code (int): HTTP status code.

        Returns:
            Type[CensysAPIException]: Exception to raise.
        """

        return self.EXCEPTIONS.get(status_code, CensysAPIException)

    def _make_call(
        self,
        method: Callable,
        endpoint: str,
        args: Optional[dict] = None,
        data: Optional[Any] = None,
    ) -> dict:
        """
        Wrapper functions for all our REST API calls checking for errors
        and decoding the responses.

        Args:
            method (Callable): Method to send HTTP request.
            endpoint (str): The path of API endpoint.
            args (dict, optional): URL args that are mapped to params.
            data (Any, optional): JSON data to serialize with request.

        Raises:
            CensysJSONDecodeException: The response is not valid JSON.

        Returns:
            dict: Search results from an API query.
        """

        if endpoint.startswith("/"):
            url = "".join((self._api_url, endpoint))
        else:
            url = "/".join((self._api_url, endpoint))

        request_kwargs = {
            "params": args or {},
            "timeout": self.timeout,
        }

        if data:
            data = json.dumps(data)
            request_kwargs["data"] = data

        res = method(url, **request_kwargs)

        if res.status_code == 200:
            return res.json()

        try:
            message = res.json()["error"]
            const = res.json().get("error_type", None)
        except (ValueError, json.decoder.JSONDecodeError) as error:  # pragma: no cover
            message = (
                f"Response from {res.url} is not valid JSON and cannot be decoded."
            )
            raise CensysJSONDecodeException(
                status_code=res.status_code,
                message=message,
                body=res.text,
                const="badjson",
            ) from error
        except KeyError:  # pragma: no cover
            message = None
            const = "unknown"
        censys_exception = self._get_exception_class(res.status_code)
        raise censys_exception(
            status_code=res.status_code, message=message, body=res.text, const=const,
        )

    def _get(self, endpoint: str, args: Optional[dict] = None) -> dict:
        return self._make_call(self._session.get, endpoint, args)

    def _post(self, endpoint: str, args: Optional[dict] = None, data=None) -> dict:
        return self._make_call(self._session.post, endpoint, args, data)

    def _delete(self, endpoint: str, args: Optional[dict] = None) -> dict:
        return self._make_call(self._session.delete, endpoint, args)  # pragma: no cover

    def account(self) -> dict:
        """
        Gets the current account information. Including email and quota.

        Returns:
            dict: Account response.
        """

        return self._get("account")

    def quota(self) -> dict:
        """
        Gets the current account's query quota.

        Returns:
            dict: Quota response.
        """

        return self.account()["quota"]


class CensysIndex(CensysAPIBase):
    """
    This class is the base class for the Data, Certificate, IPv4, and Website index.
    """

    INDEX_NAME: Optional[str] = None
    """Name of Censys Index."""

    def __init__(self, *args, **kwargs):
        CensysAPIBase.__init__(self, *args, **kwargs)
        # Generate concrete paths to be called
        self.search_path = f"search/{self.INDEX_NAME}"
        self.view_path = f"view/{self.INDEX_NAME}"
        self.report_path = f"report/{self.INDEX_NAME}"

    def metadata(self, query: str) -> dict:
        """
        Returns metadata of a given search query.

        Args:
            query (str): The query to be executed.

        Returns:
            dict: The metadata of the result set returned.
        """

        data = {"query": query, "page": 1, "fields": []}
        return self._post(self.search_path, data=data).get("metadata", {})

    def paged_search(
        self, query: str, fields: Fields = None, page: int = 1, flatten: bool = True,
    ) -> dict:
        """
        Searches the given index for all records that match the given query.

        Args:
            query (str): The query to be executed.
            fields (Fields, optional): Fields to be returned in the result set.
            page (int, optional): The page of the result set. Defaults to 1.
            flatten (bool, optional): Flattens fields to dot notation. Defaults to True.

        Returns:
            dict: The result set returned.
        """

        page = int(page)
        data = {
            "query": query,
            "page": page,
            "fields": fields or [],
            "flatten": flatten,
        }
        return self._post(self.search_path, data=data)

    def search(
        self,
        query: str,
        fields: Fields = None,
        page: int = 1,
        max_records: Optional[int] = None,
        flatten: bool = True,
    ) -> Generator[dict, None, None]:
        """
        Searches the given index for all records that match the given query.
        For more details, see our documentation: https://censys.io/api/v1/docs/search

        Args:
            query (str): The query to be executed.
            fields (Fields, optional): Fields to be returned in the result set.
            page (int, optional): The page of the result set. Defaults to 1.
            max_records (Optional[int], optional): The maximum number of records.
            flatten (bool, optional): Flattens fields to dot notation. Defaults to True.

        Yields:
            dict: The result set returned.
        """

        if fields is None:
            fields = []
        page = int(page)
        pages = float("inf")
        data = {"query": query, "page": page, "fields": fields, "flatten": flatten}

        count = 0
        while page <= pages:
            payload = self._post(self.search_path, data=data)
            pages = payload["metadata"]["pages"]
            page += 1
            data["page"] = page

            for result in payload["results"]:
                yield result
                count += 1
                if max_records and count >= max_records:
                    return

    def view(self, document_id: str) -> dict:
        """
        View the current structured data we have on a specific document.
        For more details, see our documentation: https://censys.io/api/v1/docs/view

        Args:
            document_id (str): The ID of the document you are requesting.

        Returns:
            dict: The result set returned.
        """

        return self._get("/".join((self.view_path, document_id)))

    def report(self, query: str, field: str, buckets: int = 50) -> dict:
        """
        Creates a report on the breakdown of the values of a field in a result set.
        For more details, see our documentation: https://censys.io/api/v1/docs/report

        Args:
            query (str): The query to be executed.
            field (str): The field you are running a breakdown on.
            buckets (int, optional): The maximum number of values. Defaults to 50.

        Returns:
            dict: The result set returned.
        """

        data = {"query": query, "field": field, "buckets": int(buckets)}
        return self._post(self.report_path, data=data)
