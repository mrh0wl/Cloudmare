"""Interact with the Censys Logbook API."""
import datetime
from typing import Iterator, List, Optional, Union

from .api import CensysAsmAPI


class Events(CensysAsmAPI):
    """Events API class."""

    base_path = "logbook"

    def get_cursor(
        self,
        start: Optional[Union[datetime.datetime, int]] = None,
        filters: Optional[List[str]] = None,
    ) -> str:
        """Requests a logbook cursor.

        Args:
            start ([datetime.datetime, int]): Optional; Timestamp or event ID to begin searching.
            filters (list): Optional; List of filters applied to logbook search results.

        Returns:
            str: Cursor result.
        """
        path = f"{self.base_path}-cursor"
        data = format_data(start=start, filters=filters)

        return self._post(path, data=data)["cursor"]

    def get_events(self, cursor: Optional[str] = None) -> Iterator[dict]:
        """Requests logbook events from inception or from the provided cursor.

        Args:
            cursor (str): Optional; Logbook cursor.

        Yields:
            dict: Logbook event.
        """
        args = {"cursor": cursor}

        yield from self._get_logbook_page(self.base_path, args)


class Filters:
    """Logbook filters class."""

    CERT = "CERT"
    CERT_RISK = "CERT_RISK"
    DOMAIN = "DOMAIN"
    DOMAIN_EXPIRATION_DATE = "DOMAIN_EXPIRATION_DATE"
    DOMAIN_MAIL_EXCHANGE_SERVER = "DOMAIN_MAIL_EXCHANGE_SERVER"
    DOMAIN_NAME_SERVER = "DOMAIN_NAME_SERVER"
    DOMAIN_REGISTRAR = "DOMAIN_REGISTRAR"
    DOMAIN_RISK = "DOMAIN_RISK"
    DOMAIN_SUBDOMAIN = "DOMAIN_SUBDOMAIN"
    HOST = "HOST"
    HOST_CERT = "HOST_CERT"
    HOST_PORT = "HOST_PORT"
    HOST_PROTOCOL = "HOST_PROTOCOL"
    HOST_RISK = "HOST_RISK"
    HOST_SOFTWARE = "HOST_SOFTWARE"
    HOST_VULNERABILITY = "HOST_VULNERABILITY"


def format_data(
    start: Optional[Union[datetime.datetime, int]] = None,
    filters: Optional[List[str]] = None,
) -> dict:
    """Formats cursor request data into a start date/id and filter list.

    Args:
        start ([datetime.datetime, int]): Optional; Timestamp or event ID to begin searching.
        filters (list): Optional; List of filters applied to logbook search results.

    Returns:
        dict: Formatted logbook cursor request data
    """
    data: dict = {}

    if filters:
        data["filter"] = {"type": filters}
    if isinstance(start, int):
        data["idFrom"] = start
    elif start:
        data["dateFrom"] = start

    return data
