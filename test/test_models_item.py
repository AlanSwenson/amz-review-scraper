import pytest

from test.support.configure_test import app
from amz_review_scraper import db
from amz_review_scraper.models.user import User
import amz_review_scraper.models.item as item
from amz_review_scraper.config import TestingConfig
import amz_review_scraper.model_functions as model_functions


def test_db_create(app):
    app = app(TestingConfig)

    scraped_item = item.Item(
        name="test name", customer_reviews_count="99", asin="1111111111"
    )
    scraped_item = item.save_or_update(scraped_item)
    model_functions.save_to_db()

    assert db.session.query(item.Item).one()
