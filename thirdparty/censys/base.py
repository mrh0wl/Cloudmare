import json
import os
import unittest

import thirdparty.requests as requests

from . import __name__, __version__


class CensysException(Exception):

    def __init__(self, status_code, message, headers=None, body=None, const=None):
        self.status_code = status_code
        self.message = message
        self.headers = headers or {}
        self.body = body
        self.const = const

    def __repr__(self):
        return "%i (%s): %s" % (self.status_code, self.const, self.message or self.body)

    __str__ = __repr__


class CensysRateLimitExceededException(CensysException):
    pass


class CensysNotFoundException(CensysException):
    pass


class CensysUnauthorizedException(CensysException):
    pass


class CensysJSONDecodeException(CensysException):
    pass


class CensysAPIBase(object):

    DEFAULT_URL = "https://www.censys.io/api/v1"
    DEFAULT_TIMEOUT = 30
    DEFAULT_USER_AGENT = '%s/%s' % (__name__, __version__)

    EXCEPTIONS = {
        403: CensysUnauthorizedException,
        404: CensysNotFoundException,
        429: CensysRateLimitExceededException
    }

    def __init__(self, api_id=None, api_secret=None, url=None, timeout=None, user_agent_identifier=None):
        self.api_id = api_id or os.environ.get("CENSYS_API_ID", None)
        self.api_secret = api_secret or os.environ.get("CENSYS_API_SECRET", None)
        if not self.api_id or not self.api_secret:
            raise CensysException(401, "No API ID or API secret configured.")
        timeout = timeout or self.DEFAULT_TIMEOUT
        self._api_url = url or os.environ.get("CENSYS_API_URL", None) or self.DEFAULT_URL
        # create a session that we'll use for making requests
        self._session = requests.Session()
        self._session.auth = (self.api_id, self.api_secret)
        self._session.timeout = timeout
        self._session.headers.update({
            "accept": "application/json, */8",
            "User-Agent": ' '.join(
                [requests.utils.default_user_agent(), user_agent_identifier or self.DEFAULT_USER_AGENT])
        })
        # test that everything works by requesting the users account information
        self.account()

    def _get_exception_class(self, i):
        return self.EXCEPTIONS.get(i, CensysException)

    # wrapper functions that handle making all our REST calls to the API,
    # checking for errors, and decoding the results
    def _make_call(self, method, endpoint, args=None, data=None):
        if endpoint.startswith("/"):
            url = "".join((self._api_url, endpoint))
        else:
            url = "/".join((self._api_url, endpoint))
        args = args or {}
        if data:
            data = json.dumps(data or {})
            res = method(url, params=args, data=data)
        else:
            res = method(url, params=args)
        if res.status_code == 200:
            return res.json()
        else:
            try:
                message = res.json()["error"]
                const = res.json().get("error_type", None)
            except ValueError:
                raise CensysJSONDecodeException(
                        status_code=res.status_code,
                        message="Censys response is not valid JSON and cannot be decoded.",
                        headers=res.headers,
                        body=res.text,
                        const="badjson"
                )
            except KeyError:
                message = None
                const = "unknown"
            censys_exception = self._get_exception_class(res.status_code)
            raise censys_exception(
                status_code=res.status_code,
                message=message,
                headers=res.headers,
                body=res.text,
                const=const)

    def _get(self, endpoint, args=None):
        return self._make_call(self._session.get, endpoint, args)

    def _post(self, endpoint, args=None, data=None):
        return self._make_call(self._session.post, endpoint, args, data)

    def _delete(self, endpoint, args=None):
        return self._make_call(self._session.delete, endpoint, args)

    def account(self):
        return self._get("account")


class CensysIndex(CensysAPIBase):

    INDEX_NAME = None

    def __init__(self, *args, **kwargs):
        CensysAPIBase.__init__(self, *args, **kwargs)
        # generate concrete paths to be called
        self.search_path = "search/%s" % self.INDEX_NAME
        self.view_path   = "view/%s" % self.INDEX_NAME
        self.report_path = "report/%s" % self.INDEX_NAME

    def metadata(self, query):
        data = {
            "query": query,
            "page": 1,
            "fields":[]
        }
        return self._post(self.search_path, data=data).get("metadata", {})

    def paged_search(self, query, fields=None, page=1, flatten=True):
        if fields is None:
            fields = []
        page = int(page)
        data = {
            "query": query,
            "page": page,
            "fields": fields,
            "flatten": flatten
        }
        return self._post(self.search_path, data=data)

    def search(self, query, fields=None, page=1, max_records=None, flatten=True):
        """returns iterator over all records that match the given query"""
        if fields is None:
            fields = []
        page = int(page)
        pages = float('inf')
        data = {
            "query": query,
            "page": page,
            "fields": fields,
            "flatten": flatten
        }

        count = 0
        while page <= pages:
            payload = self._post(self.search_path, data=data)
            pages = payload['metadata']['pages']
            page += 1
            data["page"] = page

            for result in payload["results"]:
                yield result
                count += 1
                if max_records and count >= max_records:
                    return

    def view(self, ip):
        return self._get("/".join((self.view_path, ip)))

    def report(self, query, field, buckets=50):
        data = {
            "query": query,
            "field": field,
            "buckets": int(buckets)
        }
        return self._post(self.report_path, data=data)


class CensysAPIBaseTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._api = CensysAPIBase()

    def test_my_account(self):
        res = self._api.account()
        self.assertEqual(res["api_id"], self._api.api_id)
        self.assertEqual(res["api_secret"], self._api.api_secret)


if __name__ == "__main__":
    unittest.main()

