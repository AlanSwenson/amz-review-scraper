import pytest

from amz_review_scraper import create_app, db
from amz_review_scraper.config import TestingConfig


@pytest.yield_fixture
def app():
    def _app(config_class):

        app = create_app(config_class)
        app.test_request_context().push()

        if config_class is TestingConfig:

            # always starting with an empty DB
            db.drop_all()
            from amz_review_scraper.models.users_items_association import (
                users_items_association,
            )
            from amz_review_scraper.models.user import User
            from amz_review_scraper.models.item import Item
            from amz_review_scraper.models.review import Review
            from amz_review_scraper.models.token_blacklist import TokenBlacklist

            db.create_all()
            # mocker.patch("flask_jwt_extended.get_jwt_identity", return_value=1)

        return app

    yield _app
    db.session.remove()
    if str(db.engine.url) == TestingConfig.SQLALCHEMY_DATABASE_URI:
        db.drop_all()
