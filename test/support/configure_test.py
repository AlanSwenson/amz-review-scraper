import pytest

from amz_review_scraper import create_app, db
from amz_review_scraper.config import get_env_db_url
from amz_review_scraper.config import TestingConfig


@pytest.yield_fixture
def app():
    def _app(config_class):
        app = create_app(config_class)
        app.app_context().push()

        if config_class is TestingConfig:

            # always starting with an empty DB
            db.drop_all()
            from amz_review_scraper.models.users_items_association import (
                users_items_association,
            )
            from amz_review_scraper.models.user import User
            from amz_review_scraper.models.item import Item
            from amz_review_scraper.models.review import Review

            db.create_all()

        return app

    yield _app
    db.session.remove()
    if str(db.engine.url) == TestingConfig.SQLALCHEMY_DATABASE_URI:
        db.drop_all()
