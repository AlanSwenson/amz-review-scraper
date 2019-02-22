import pytest

from test.support.configure_test import app
from amz_review_scraper import db
from amz_review_scraper.models.user import User
import amz_review_scraper.models.item as item
from amz_review_scraper.config import TestingConfig
import amz_review_scraper.model_functions as model_functions
from test.support.testing_functions import create_test_user
import amz_review_scraper.models.review as review

# create db
def test_reviews(app):
    app = app(TestingConfig)

    # create a user
    create_test_user(email="test_email@email.com", plain_password="test_password")
    user = User.query.filter_by(email="test_email@email.com").one_or_none()
    # create an item
    scraped_item = item.Item(
        name="test name", customer_reviews_count="99", asin="1111111111"
    )
    # TODO: break this out in amzscraper.py to be a stand alone testable method
    existing_item = item.get_results(asin=scraped_item.asin)
    # add an item
    if existing_item is None:
        user.items.append(scraped_item)
    else:
        item_link = item.is_item_linked_to_user(scraped_item, user)
        if item_link is None:
            user.items.append(existing_item)
        scraped_item = item.save_or_update(scraped_item)

    # add Review using save
    scraped_review = review.Review(
        review="testing_long_review", asin=scraped_item.asin, owner=scraped_item
    )
    review.save(scraped_review)
    model_functions.save_to_db()

    # check that reviews exists using get results
    assert db.session.query(review.Review).filter_by(review="testing_long_review").one()
    assert review.get_results(asin="1111111111").one().review == "testing_long_review"
    assert (
        review.get_results(asin="1111111111", review="testing_long_review").review
        == "testing_long_review"
    )
    # TODO: add more tests for when it shoud fail
