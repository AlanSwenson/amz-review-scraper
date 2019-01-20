import pytest

from test.support.configure_test import app
from amz_review_scraper import db, bcrypt
import amz_review_scraper.models.user as user
from amz_review_scraper.config import TestingConfig
import amz_review_scraper.model_functions as model_functions


def test_add_user(app):
    app = app(TestingConfig)

    hashed_password = bcrypt.generate_password_hash("test_password").decode("utf-8")
    test_user = user.User(email="test_email@email.com", password=hashed_password)
    db.session.add(test_user)
    db.session.commit()

    assert db.session.query(user.User).filter_by(email="test_email@email.com").one()
