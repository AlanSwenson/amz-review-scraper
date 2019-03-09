"""Async Tasks to use in Zappa"""

from flask import flash

from zappa.async import task

from amz_review_scraper import create_app
from amz_review_scraper.get_soup import boil_soup
from amz_review_scraper.amzscraper import scrape
from amz_review_scraper.config import DevelopmentConfig


@task
def track_asin(url, asin, user_id, config_class=DevelopmentConfig):
    app = create_app(config_class)
    with app.app_context():
        soup = boil_soup(url, asin)
        if soup.status_code is not None:
            flash(
                "ASIN returned Status Code: "
                + str(soup.status_code)
                + " Please check your ASIN and try Again"
            )
        else:
            scrape(soup, asin, user_id)
