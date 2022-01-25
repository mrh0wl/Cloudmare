"""Interact with the Censys Search Data API."""
from .api import CensysSearchAPIv1


class CensysData(CensysSearchAPIv1):
    """Interacts with the Data index.

    For more details, see our documentation: https://search.censys.io/api
    """

    _PREFIX = "/data"
    """Endpoint prefix."""

    def get_series(self) -> dict:
        """Get data on the types of scans we regularly perform (series).

        Returns:
            dict: The result set returned.
        """
        return self._get(self._PREFIX)

    def view_series(self, series_id: str) -> dict:
        """Get data on a specific series.

        Args:
            series_id (str): The ID of the series.

        Returns:
            dict: The result set returned.
        """
        path = f"{self._PREFIX}/{series_id}"
        return self._get(path)

    def view_result(self, series_id: str, result_id: str) -> dict:
        """View a specific result of a specific series.

        Args:
            series_id (str): The ID of the series.
            result_id (str): The ID of the result.

        Returns:
            dict: The result set returned.
        """
        path = f"{self._PREFIX}/{series_id}/{result_id}"
        return self._get(path)
