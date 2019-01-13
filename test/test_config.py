import pytest

from test.support.configure_test import app
from amz_review_scraper.config import get_env_db_url


def test_development_config(app):
    app.config.from_object("amz_review_scraper.config.DevelopmentConfig")

    DB_URL = get_env_db_url("development")

    assert app.config["DEBUG"]
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == DB_URL


def test_testing_config(app):
    app.config.from_object("amz_review_scraper.config.TestingConfig")

    DB_URL = get_env_db_url("testing")

    assert app.config["DEBUG"]
    assert app.config["TESTING"]
    assert not app.config["PRESERVE_CONTEXT_ON_EXCEPTION"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == DB_URL


def test_production_config(app):
    app.config.from_object("amz_review_scraper.config.ProductionConfig")

    DB_URL = get_env_db_url("production")

    assert not app.config["DEBUG"]
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == DB_URL
