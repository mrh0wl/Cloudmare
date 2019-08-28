from __future__ import print_function
import unittest

from .base import CensysAPIBase, CensysIndex, CensysException

class CensysWebsites(CensysIndex):

    INDEX_NAME = "websites"


class CensysWebsitesTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._api = CensysWebsites()

    def testGet(self):
        self._api.view("google.com")

    def testSearch(self):
        list(self._api.search("*", max_records=10))

    def testReport(self):
        self._api.report("*", "80.http.get.headers.server.raw")


if __name__ == "__main__":
    unittest.main()
