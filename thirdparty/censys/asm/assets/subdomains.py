"""Interact with the Censys Subdomain Assets API."""
from typing import Any, Dict, Iterator, List, Optional

from .assets import Assets


class SubdomainsAssets(Assets):
    """Subdomains Assets API class."""

    def __init__(self, domain: str, *args, **kwargs):
        """Inits SubdomainsAssets.

        Args:
            domain: Name of the parent domain
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__("subdomains", *args, **kwargs)
        # Rewrite the path because it chains off of the parent domain
        self.base_path = f"assets/domains/{domain}/subdomains"

    def get_assets(
        self,
        page_number: int = 1,
        page_size: Optional[int] = None,
        tag: Optional[List[str]] = None,
        tag_operator: Optional[str] = None,
        source: Optional[List[str]] = None,
    ) -> Iterator[dict]:
        """Requests assets data.

        Override for subdomains due to it return value in a different key.

        Args:
            page_number (int): Optional; Page number to begin at when searching.
            page_size (int): Optional; Page size for retrieving assets.
            tag (list): Optional; List of tags to search for.
            tag_operator (str): Optional; Operator to use when searching for tags.
            source (list): Optional; List of sources to search for.

        Yields:
            dict: The assets result returned.
        """
        args: Dict[str, Any] = {}
        if tag:
            args["tag"] = tag
        if tag_operator:
            args["tagOperator"] = tag_operator
        if source:
            args["source"] = source
        yield from self._get_page(
            self.base_path,
            page_number=page_number,
            page_size=page_size,
            args=args,
            keyword="subdomains",
        )
