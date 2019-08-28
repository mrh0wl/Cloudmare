import unittest
import json

from .base import CensysAPIBase

class CensysData(CensysAPIBase):

    _PREFIX = '/data'

    def get_series(self):
        return self._get(self._PREFIX)

    def view_series(self, series):
        path = '/'.join([
            self._PREFIX,
            series,
        ])
        return self._get(path)

    def view_result(self, series, result):
        path = '/'.join([
            self._PREFIX,
            series,
            result,
        ])
        return self._get(path)


class CensysDataTest(unittest.TestCase):

    EXPECTED_GET_SERIES_KEYS = ['primary_series', 'raw_series']

    EXPECTED_VIEW_SERIES = {
        "port": 22,
        "subprotocol": "banner",
        "protocol": "ssh",
        "name": "22-ssh-banner-full_ipv4",
        "destination": "full_ipv4",
        "id": "22-ssh-banner-full_ipv4",
        "description": "This dataset is composed of a ZMap TCP SYN scan on port 22 and a ZGrab SSH Banner Grab\r\nfor the for responsive hosts. The connection is terminated after a banner has been\r\nreceived. We do not currently capture SSH host keys, but we are planning to add this\r\nfunctionality in the future.",
    }

    EXPECTED_VIEW_RESULT = {
        "files": {
            "ztee-zgrab-updates": {
                "compressed_size": None,
                "sha256_fingerprint": "61631fa0bdc933f2df25b77ac941702f5b55ad733ceed1db17f510cfa93c6f21",
                "download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-ztee-zgrab-updates.csv.lz4",
                "file_type": "csv",
                "compressed_sha256_fingerprint": None,
                "compressed_download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-ztee-zgrab-updates.csv.lz4",
                "size": 1,
                "compression_type": None,
                "schema": None
            },
            "zgrab-results": {
                "compressed_size": None,
                "sha256_fingerprint": "6f39fe8583dae94fdc4a7f5e6f62d662cb62b15a92d2f4bf00fd8889fe7b2459",
                "download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-zgrab-results.json.lz4",
                "file_type": "json",
                "compressed_sha256_fingerprint": None,
                "compressed_download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-zgrab-results.json.lz4",
                "size": 34506,
                "compression_type": None,
                "schema": None
            },
            "zgrab-metadata": {
                "compressed_size": None,
                "sha256_fingerprint": "a72e5516d23e333f4ac00d08e352bdc2e3eaaa1c14aa339fe7d6828b52f00e2a",
                "download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-zgrab-metadata.json.lz4",
                "file_type": "json",
                "compressed_sha256_fingerprint": None,
                "compressed_download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-zgrab-metadata.json.lz4",
                "size": 0,
                "compression_type": None,
                "schema": None
            },
            "zmap-log": {
                "compressed_size": None,
                "sha256_fingerprint": "838987ae6187976222abd037c32b06b654bdd940cb24415e43a8aac1efe85b78",
                "download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-zmap-log.log.lz4",
                "file_type": "log",
                "compressed_sha256_fingerprint": None,
                "compressed_download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-zmap-log.log.lz4",
                "size": 0,
                "compression_type": None,
                "schema": None
            },
            "zgrab-log": {
                "compressed_size": None,
                "sha256_fingerprint": "417ab72c11f758b2385832056bd9ccfc131480ce76114ecfde99f1b4a637a4eb",
                "download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-zgrab-log.log.lz4",
                "file_type": "log",
                "compressed_sha256_fingerprint": None,
                "compressed_download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-zgrab-log.log.lz4",
                "size": 1954,
                "compression_type": None,
                "schema": None
            },
            "ztee-zmap-updates": {
                "compressed_size": None,
                "sha256_fingerprint": "d5a01a4b3fc5b5537b8bad6116d8fed78207add9bcd45679141735764de87cd3",
                "download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-ztee-zmap-updates.csv.lz4",
                "file_type": "csv",
                "compressed_sha256_fingerprint": None,
                "compressed_download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-ztee-zmap-updates.csv.lz4",
                "size": 1,
                "compression_type": None,
                "schema": None
            },
            "ztag-metadata": {
                "compressed_size": None,
                "sha256_fingerprint": "b63458035d724313135a1aecfad0490038219f917f7f4dba1db374ce1b6b2637",
                "download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-ztag-metadata.json.lz4",
                "file_type": "json",
                "compressed_sha256_fingerprint": None,
                "compressed_download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-ztag-metadata.json.lz4",
                "size": 0,
                "compression_type": None,
                "schema": None
            },
            "zmap-metadata": {
                "compressed_size": None,
                "sha256_fingerprint": "33a9f67ecb1a0b80ffc612831c217e093802d2a9fd9b2f940af73e0277df1981",
                "download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-zmap-metadata.json.lz4",
                "file_type": "json",
                "compressed_sha256_fingerprint": None,
                "compressed_download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-zmap-metadata.json.lz4",
                "size": 0,
                "compression_type": None,
                "schema": None
            },
            "zmap-results": {
                "compressed_size": None,
                "sha256_fingerprint": "22778c15a2570b9b4a0478f17f2058f59b3ece76327a730dbd6fe810bdf39ca1",
                "download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-zmap-results.csv.lz4",
                "file_type": "csv",
                "compressed_sha256_fingerprint": None,
                "compressed_download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-zmap-results.csv.lz4",
                "size": 311,
                "compression_type": None,
                "schema": None
            },
            "ztag-log": {
                "compressed_size": None,
                "sha256_fingerprint": "9bc0cf25f56dfcb6c5d6086588ae3686ff89101db50458d361807e7af2c1a4c1",
                "download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-ztag-log.log.lz4",
                "file_type": "log",
                "compressed_sha256_fingerprint": None,
                "compressed_download_path": "https://scans.io/zsearch/pibuyr5kj674258t-22-ssh-banner-full_ipv4-20170404T224559-ztag-log.log.lz4",
                "size": 0,
                "compression_type": None,
                "schema": None
            }
        },
        "task_id": None,
        "series": {
            "id": "22-ssh-banner-full_ipv4",
            "name": "22-ssh-banner-full_ipv4"
        },
        "timestamp": "20170405T185945",
        "id": "20170405T1859",
        "metadata": {}
    }


    @classmethod
    def setUpClass(cls):
        cls._api = CensysData()

    def testGetSeries(self):
        series = self._api.get_series()
        for key in self.EXPECTED_GET_SERIES_KEYS:
            self.assertTrue(key in series)

    def testViewSeries(self):
        series = "22-ssh-banner-full_ipv4"
        res = self._api.view_series(series)
        for k, v in self.EXPECTED_VIEW_SERIES.iteritems():
            self.assertEqual(res[k], v)
        results = res['results']
        self.assertTrue('latest' in results)
        historical = results['historical']
        self.assertTrue(len(historical) > 0)

    def testViewResult(self):
        series = "22-ssh-banner-full_ipv4"
        result = "20170405T1859"
        res = self._api.view_result(series, result)
        self.assertEqual(self.EXPECTED_VIEW_RESULT, res)


if __name__ == "__main__":
    unittest.main()
