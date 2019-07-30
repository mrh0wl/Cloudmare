from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
import pytest

def test_answer():
    domain = 'uber.com'
    res = DNSDumpsterAPI(True).search(domain)
    assert len(res['dns_records']['host']) > 0