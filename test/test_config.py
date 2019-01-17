import pytest
import os

from test.support.configure_test import app
from amz_review_scraper.config import (
    get_env_db_url,
    TestingConfig,
    DevelopmentConfig,
    ProductionConfig,
)
from amz_review_scraper import db
import amz_review_scraper.models.item as item
from amz_review_scraper.models.user import User
import amz_review_scraper.model_functions as model_functions


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == True,
    reason="Skipping this test on Travis CI.",
)
def test_development_config(app):
    app = app(DevelopmentConfig)
    DB_URL = get_env_db_url("development")
    print(DB_URL)
    assert app.config["DEBUG"]
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == DB_URL


def test_testing_config(app):
    app = app(TestingConfig)
    DB_URL = get_env_db_url("testing")
    print(DB_URL)
    assert app.config["DEBUG"]
    assert app.config["TESTING"]
    assert not app.config["PRESERVE_CONTEXT_ON_EXCEPTION"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == DB_URL


def test_production_config(app):
    app = app(ProductionConfig)
    DB_URL = get_env_db_url("production")
    print(DB_URL)
    assert not app.config["DEBUG"]
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == DB_URL


def test_db_create(app):
    app = app(TestingConfig)

    scraped_item = item.Item(
        name="test name", customer_reviews_count="99", asin="1111111111"
    )
    scraped_item = item.save_or_update(scraped_item)
    model_functions.save_to_db()

    assert db.session.query(item.Item).one()
