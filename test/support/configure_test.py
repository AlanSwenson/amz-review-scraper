import pytest

from amz_review_scraper import create_app


@pytest.fixture
def app():
    app = create_app()
    # app.config.from_object("amz_review_scraper.config.TestingConfig")
    return app
