"""Interact with the Censys Clouds API."""
import datetime
from typing import Union

from .api import CensysAsmAPI

Since = Union[str, datetime.date, datetime.datetime]


def format_since_date(since: Since) -> str:
    """Formats since date as ISO 8601 format.

    Args:
        since (Since): Date.

    Returns:
        str: ISO 8601 formatted date string.
    """
    if isinstance(since, (datetime.date, datetime.datetime)):
        return since.strftime("%Y-%m-%d")
    return since


class Clouds(CensysAsmAPI):
    """Clouds API class."""

    base_path = "clouds"

    def get_host_counts(
        self,
        since: Since,
    ) -> dict:
        """Retrieve host counts by cloud.

        Hosts found after the date provided in the `since` parameter will be included in the new asset counts.

        Args:
            since (Since): Date to include hosts from.

        Returns:
            dict: Host count result.
        """
        since = format_since_date(since)
        return self._get(f"{self.base_path}/hostCounts/{since}")

    def get_domain_counts(self, since: Since) -> dict:
        """Retrieve domain counts by cloud.

        Args:
            since (Since): Date to include domains from.

        Returns:
            dict: Domain count result.
        """
        since = format_since_date(since)
        return self._get(f"{self.base_path}/domainCounts/{since}")

    def get_object_store_counts(self, since: Since) -> dict:
        """Retrieve object store counts by cloud.

        Args:
            since (Since): Date to include object stores from.

        Returns:
            dict: Object store count result.
        """
        since = format_since_date(since)
        return self._get(f"{self.base_path}/objectStoreCounts/{since}")

    def get_subdomain_counts(self, since: Since) -> dict:
        """Retrieve subdomain counts by cloud.

        Args:
            since (Since): Date to include subdomains from.

        Returns:
            dict: Subdomain count result.
        """
        since = format_since_date(since)
        return self._get(f"{self.base_path}/subdomainCounts/{since}")

    def get_unknown_counts(self) -> dict:
        """Retrieve known and unknown counts for hosts by cloud.

        Returns:
            dict: Unknown count result.
        """
        return self._get(f"{self.base_path}/unknownCounts")
