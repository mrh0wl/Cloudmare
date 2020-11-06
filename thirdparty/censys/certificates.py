"""
Interact with the Censys Search Certificate API.
"""

from typing import List

from thirdparty.censys.base import CensysIndex


class CensysCertificates(CensysIndex):
    """
    Interacts with the Certificates index.
    """

    INDEX_NAME = "certificates"
    """Name of Censys Index."""
    MAX_PER_BULK_REQUEST = 50
    """Max number of bulk thirdparty.requests."""

    def __init__(self, *args, **kwargs):
        CensysIndex.__init__(self, *args, **kwargs)
        self.bulk_path = f"/bulk/{self.INDEX_NAME}"

    def bulk(self, fingerprints: List[str]) -> dict:
        """
        thirdparty.requests data in bulk.

        Args:
            fingerprints (List[str]): List of certificate SHA256 fingerprints.

        Returns:
            dict: Search results from an API query.
        """

        result = dict()
        start = 0
        end = self.MAX_PER_BULK_REQUEST
        while start < len(fingerprints):
            data = {"fingerprints": fingerprints[start:end]}
            result.update(self._post(self.bulk_path, data=data))
            start = end
            end += self.MAX_PER_BULK_REQUEST

        return result
