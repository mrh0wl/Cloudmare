"""Interact with the Censys Search Host API."""
from typing import Any, List, Optional

from .api import CensysSearchAPIv2
from ...common.types import Datetime
from ...common.utils import format_rfc3339


class CensysHosts(CensysSearchAPIv2):
    """Interacts with the Hosts index.

    Examples:
        Inits Censys Hosts.

        >>> from censys.search import CensysHosts
        >>> h = CensysHosts()

        Simple host search.

        >>> for page in h.search("service.service_name: HTTP"):
        >>>     print(page)
        [
            {
            'services':
                [
                    {'service_name': 'HTTP', 'port': 80},
                    {'service_name': 'HTTP', 'port': 443}
                ],
            'ip': '1.0.0.0'
            },
            ...
        ]

        Fetch a specific host and its services

        >>> h.view("1.0.0.0")
        {
            'ip': '8.8.8.8',
            'services': [{}],
            ...
        }

        Simple host aggregate.

        >>> h.aggregate("service.service_name: HTTP", "services.port", num_buckets=5)
        {
            'total_omitted': 591527370,
            'buckets': [
                {'count': 56104072, 'key': '80'},
                {'count': 43527894, 'key': '443'},
                {'count': 23070429, 'key': '7547'},
                {'count': 12970769, 'key': '30005'},
                {'count': 12825150, 'key': '22'}
            ],
            'potential_deviation': 3985101,
            'field': 'services.port',
            'query': 'service.service_name: HTTP',
            'total': 172588754
        }

        Fetch a list of host names for the specified IP address.

        >>> h.view_host_names("1.1.1.1")
        ['one.one.one.one']

        Fetch a list of events for the specified IP address.

        >>> h.view_host_events("1.1.1.1")
        [{'timestamp': '2019-01-01T00:00:00.000Z'}]
    """

    INDEX_NAME = "hosts"
    """Name of Censys Index."""

    def search(
        self,
        query: str,
        per_page: Optional[int] = None,
        cursor: Optional[str] = None,
        pages: int = 1,
        virtual_hosts: Optional[str] = None,
        **kwargs: Any,
    ) -> CensysSearchAPIv2.Query:
        """Search host index.

        Searches the given index for all records that match the given query.
        For more details, see our documentation: https://search.censys.io/api

        Args:
            query (str): The query to be executed.
            per_page (int): Optional; The number of results to be returned for each page. Defaults to 100.
            cursor (int): Optional; The cursor of the desired result set.
            virtual_hosts (str): Optional; Whether to include virtual hosts in the results. Valid values are "EXCLUDE", "INCLUDE", and "ONLY".
            pages (int): Optional; The number of pages returned. Defaults to 1.
            **kwargs (Any): Optional; Additional arguments to be passed to the query.

        Returns:
            Query: Query object that can be a callable or an iterable.
        """
        if virtual_hosts:
            kwargs["virtual_hosts"] = virtual_hosts
        return super().search(query, per_page, cursor, pages, **kwargs)

    def view_host_names(self, ip: str) -> List[str]:
        """Fetches a list of host names for the specified IP address.

        Args:
            ip (str): The IP address of the requested host.

        Returns:
            List[str]: A list of host names.
        """
        return self._get(self.view_path + ip + "/names")["result"]["names"]

    def view_host_diff(
        self,
        ip: str,
        ip_b: Optional[str] = None,
        at_time: Optional[Datetime] = None,
        at_time_b: Optional[Datetime] = None,
    ):
        """Fetches a diff of the specified IP address.

        Args:
            ip (str): The IP address of the requested host.
            ip_b (str): Optional; The IP address of the second host.
            at_time (Datetime): Optional; An RFC3339 timestamp which represents
                the point-in-time used as the basis for Host A.
            at_time_b (Datetime): Optional; An RFC3339 timestamp which represents
                the point-in-time used as the basis for Host B.

        Returns:
            dict: A diff of the hosts.
        """
        args = {}
        if ip_b:
            args["ip_b"] = ip_b
        if at_time:
            args["at_time"] = format_rfc3339(at_time)
        if at_time_b:
            args["at_time_b"] = format_rfc3339(at_time_b)
        return self._get(self.view_path + ip + "/diff", args)["result"]

    def view_host_events(
        self,
        ip: str,
        start_time: Optional[Datetime] = None,
        end_time: Optional[Datetime] = None,
        per_page: Optional[int] = None,
        cursor: Optional[str] = None,
        reversed: Optional[bool] = None,
    ) -> List[dict]:
        """Fetches a list of events for the specified IP address.

        Args:
            ip (str): The IP address of the requested host.
            start_time (Datetime): Optional; An RFC3339 timestamp which represents
                the beginning chronological point-in-time (inclusive) from which events are returned.
            end_time (Datetime): Optional; An RFC3339 timestamp which represents
                the ending chronological point-in-time (exclusive) from which events are returned.
            per_page (int): Optional; The maximum number of hits to return in each response
                (minimum of 1, maximum of 50).
            cursor (str): Optional; Cursor token from the API response.
            reversed (bool): Optional; Reverse the order of the return events,
                that is, return events in reversed chronological order.

        Returns:
            List[dict]: A list of events.
        """
        args = {"per_page": per_page, "cursor": cursor, "reversed": reversed}
        if start_time:
            args["start_time"] = format_rfc3339(start_time)
        if end_time:
            args["end_time"] = format_rfc3339(end_time)

        return self._get(f"/v2/experimental/{self.INDEX_NAME}/{ip}/events", args)[
            "result"
        ]["events"]

    def list_hosts_with_tag(self, tag_id: str) -> List[str]:
        """Returns a list of hosts which are tagged with the specified tag.

        Args:
            tag_id (str): The ID of the tag.

        Returns:
            List[str]: A list of host IP addresses.
        """
        hosts = self._list_documents_with_tag(tag_id, "hosts", "hosts")
        return [host["ip"] for host in hosts]
