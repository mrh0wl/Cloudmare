"""Interact with the Censys Search Cert API."""
from typing import List, Optional, Tuple

from .api import CensysSearchAPIv2


class CensysCerts(CensysSearchAPIv2):
    """Interacts with the Certs index.

    Please note that this class represents only the v2 API endpoints. The v1 API endpoints (search, view, and report) are avilable only from CensysCertificates.

    Examples:
        Inits Censys Certs.

        >>> from censys.search import CensysCerts
        >>> c = CensysCerts()

        Search for hosts by sha256fp.

        >>> c.get_hosts_by_cert("fb444eb8e68437bae06232b9f5091bccff62a768ca09e92eb5c9c2cf9d17c426")
        (
            [
                {
                    "ip": "string",
                    "name": "string",
                    "observed_at": "2021-08-02T14:56:38.711Z",
                    "first_observed_at": "2021-08-02T14:56:38.711Z",
                }
            ],
            {
                "next": "nextCursorToken",
            },
        )
    """

    INDEX_NAME = "certificates"
    """Name of Censys Index."""

    def view(self, document_id: str):  # type: ignore # noqa: D102
        """This function acts as a placeholder for the upcoming Censys Search Cert v2 API.

        To view a certificate, please use `CensysCertificates`.

        Raises:
            NotImplementedError: CensysCerts.view is not implemented yet. Please use CensysCertificates.view instead.

        :meta private:
        """
        raise NotImplementedError(
            "CensysCerts.view is not implemented yet. Please use CensysCertificates.view instead."
        )

    def search(  # type: ignore # noqa: D102
        self, query: str, per_page: Optional[int], cursor: Optional[str], pages: int
    ):
        """This function acts as a placeholder for the upcoming Censys Search Cert v2 API.

        To search for certificates, please use `CensysCertificates`.

        Raises:
            NotImplementedError: CensysCerts.search is not implemented yet. Please use CensysCertificates.search instead.

        :meta private:
        """
        raise NotImplementedError(
            "CensysCerts.search is not implemented yet. Please use CensysCertificates.search instead."
        )

    def aggregate(self, query: str, field: str, num_buckets: Optional[int]):  # type: ignore # noqa: D102
        """This function acts as a placeholder for the upcoming Censys Search Cert v2 API.

        To aggregate/report certificates, please use `CensysCertificates`.

        Raises:
            NotImplementedError: CensysCerts.aggregate is not implemented yet. Please use CensysCertificates.report instead.

        :meta private:
        """
        raise NotImplementedError(
            "CensysCerts.aggregate is not implemented yet. Please use CensysCertificates.report instead."
        )

    def metadata(self):  # noqa: D102
        """This function acts as a placeholder for the upcoming Censys Search Cert v2 API.

        Raises:
            NotImplementedError: CensysCerts.metadata is not implemented yet.

        :meta private:
        """
        raise NotImplementedError("CensysCerts.metadata is not implemented yet.")

    def get_hosts_by_cert(
        self, sha256fp: str, cursor: Optional[str] = None
    ) -> Tuple[List[str], dict]:
        """Returns a list of hosts which contain services presenting this certificate.

        Args:
            sha256fp (str): The SHA-256 fingerprint of the requested certificate.
            cursor (str): Cursor token from the API response, which fetches the next page of hosts when added to the endpoint URL.

        Returns:
            Tuple[List[str], dict]: A list of hosts and a dictionary of the pagination cursors.
        """
        args = {"cursor": cursor}
        result = self._get(self.view_path + sha256fp + "/hosts", args)["result"]
        return result["hosts"], result["links"]

    def list_certs_with_tag(self, tag_id: str) -> List[str]:
        """Returns a list of certs which are tagged with the specified tag.

        Args:
            tag_id (str): The ID of the tag.

        Returns:
            List[str]: A list of certificate SHA 256 fingerprints.
        """
        certs = self._list_documents_with_tag(tag_id, "certificates", "certs")
        return [cert["fingerprint"] for cert in certs]
