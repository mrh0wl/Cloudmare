"""Interact with the Censys Host Assets API."""
from .assets import Assets


class HostsAssets(Assets):
    """Hosts Assets API class."""

    def __init__(self, *args, **kwargs):
        """Inits HostsAssets.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__("hosts", *args, **kwargs)
