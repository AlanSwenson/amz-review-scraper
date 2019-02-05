import pytest
import os

from test.support.configure_test import app
from amz_review_scraper.config import (
    TestingConfig,
    DevelopmentConfig,
    ProductionConfig,
    env,
)


@pytest.mark.skipif(
    env.bool("TRAVIS", default=False) == True,
    # "TRAVIS" in os.environ and os.environ["TRAVIS"] == "True",
    reason="Skipping this test on Travis CI.",
)
def test_development_config(app):
    app = app(DevelopmentConfig)
    assert app.config["DEBUG"]
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == env.str(
        "DEV_SQLALCHEMY_DATABASE_URI"
    )
    assert app.config["LOGIN_BASE_URL"] == env.str("DEV_LOGIN_BASE_URL")


def test_testing_config(app):
    app = app(TestingConfig)
    assert app.config["DEBUG"]
    assert app.config["TESTING"]
    assert not app.config["PRESERVE_CONTEXT_ON_EXCEPTION"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == env.str(
        "TESTING_SQLALCHEMY_DATABASE_URI"
    )
    assert app.config["LOGIN_BASE_URL"] == env.str("TESTING_LOGIN_BASE_URL")


def test_production_config(app):
    app = app(ProductionConfig)
    assert not app.config["DEBUG"]
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == env.str(
        "PROD_SQLALCHEMY_DATABASE_URI"
    )
    assert app.config["LOGIN_BASE_URL"] == env.str("PROD_LOGIN_BASE_URL")
