import pytest
from amz_review_scraper.urls import create_url

def test_valid_url():
    url = create_url('B07HJXVHSS')
    assert url == "https://www.amazon.com/gp/product/B07HJXVHSS"
