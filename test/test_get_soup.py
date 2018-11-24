import sys

import requests
import mock
import pytest

sys.modules["config"] = mock.MagicMock()
from amz_review_scraper.get_soup import boil_soup
from test.support.mocked_requests import mocked_requests_get


@mock.patch("requests.get")
def test_does_asin_exist(self):
    self.side_effect = mocked_requests_get
    valid_asin = boil_soup(
        url="https://www.amazon.com/gp/product/B07HJXVHSS", asin="B07HJXVHSS"
    )
    invalid_asin = boil_soup(
        url="https://www.amazon.com/gp/product/B111111111", asin="B07HJXVHSS"
    )
    # A valid ASIN returns None as the status_code
    # because it actually returns the soup which no longer has a status_code
    assert valid_asin.status_code == None
    # An invalid ASIN returns a status_code
    # because it never gets converted to soup and just returns raw html
    assert invalid_asin.status_code != None
