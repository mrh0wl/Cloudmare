"""
Interact with the Censys Search IPv4 API.
"""

from thirdparty.censys.base import CensysIndex


class CensysIPv4(CensysIndex):
    """
    Interacts with the IPv4 index.
    """

    INDEX_NAME = "ipv4"
    """Name of Censys Index."""
