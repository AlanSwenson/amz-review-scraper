import pytest

from amz_review_scraper import create_app, db
from amz_review_scraper.config import get_env_db_url


@pytest.yield_fixture
def app():
    def _app(config_class):
        app = create_app(config_class)
        app.app_context().push()
        # with app.app_context():
        DB_URL = get_env_db_url("testing")

        if app.config["SQLALCHEMY_DATABASE_URI"] == DB_URL:
            # app.config.from_object("amz_review_scraper.config.TestingConfig")
            from amz_review_scraper.models.users_items_association import (
                users_items_association,
            )
            from amz_review_scraper.models.user import User
            from amz_review_scraper.models.item import Item
            from amz_review_scraper.models.review import Review

            db.create_all()
            return app
        else:
            return app
            db.session.remove()

    yield _app
    db.session.remove()
    db.drop_all()
