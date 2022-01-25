"""Interact with all Search APIs."""
from ..common.deprecation import DeprecationDecorator
from .v1 import CensysCertificates, CensysData
from .v2 import CensysCerts, CensysHosts


class SearchClient:
    """Client for interacting with all Search APIs.

    All indexes are passed the args and kwargs that are provided.

    Examples:
        Inits SearchClient.

        >>> from censys.search import SearchClient
        >>> c = SearchClient()

        Access both v1 and v2 indexes.

        >>> certs = c.v1.certificates # CensysCertificates()
        >>> data = c.v1.data # CensysData()
        >>> hosts = c.v2.hosts # CensysHosts()
        >>> certs = c.v2.certs # CensysCerts()
    """

    class _V1:
        """Class for v1 Search APIs."""

        @DeprecationDecorator(
            "The v1 Search API is deprecated and will be removed in the future."
        )
        def __init__(self, *args, **kwargs):
            """Inits V1.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.
            """
            self.certificates = CensysCertificates(*args, **kwargs)
            # Alias certs to certificates
            self.certs = self.certificates
            self.data = CensysData(*args, **kwargs)

    class _V2:
        """Class for v2 Search APIs."""

        def __init__(self, *args, **kwargs):
            """Inits V2.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.
            """
            self.hosts = CensysHosts(*args, **kwargs)
            self.certs = CensysCerts(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        """Inits SearchClient.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # Backwards compatability
        if len(args) == 2:
            kwargs["api_id"] = args[0]
            kwargs["api_secret"] = args[1]

        self.v1 = self._V1(**kwargs)
        self.v2 = self._V2(**kwargs)
