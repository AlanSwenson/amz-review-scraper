import pytest

from test.support.configure_test import app
from test.support.testing_functions import create_test_user
from amz_review_scraper import db
import amz_review_scraper.models.user as user
from amz_review_scraper.config import TestingConfig


def test_add_user(app):
    app = app(TestingConfig)

    create_test_user(email="test_email@email.com", plain_password="test_password")

    assert db.session.query(user.User).filter_by(email="test_email@email.com").one()
