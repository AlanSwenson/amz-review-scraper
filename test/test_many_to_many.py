import os
import codecs
import bs4

from test.support.configure_test import app
from test.support.testing_functions import create_test_user
from amz_review_scraper import db
import amz_review_scraper.models.user as user
from amz_review_scraper.config import TestingConfig
from amz_review_scraper.tasks import track_asin
from amz_review_scraper.urls import create_url
import amz_review_scraper.models.item as item
from amz_review_scraper.models.users_items_association import users_items_association


my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "materials/sample_output_file.html")

raw_html = codecs.open(path, "r")
soup = bs4.BeautifulSoup(raw_html, "lxml")

# TODO mock the soup results
def test_many_to_many(app):
    app = app(TestingConfig)

    create_test_user(email="test_email@email.com", plain_password="test_password")
    create_test_user(email="test2_email@email.com", plain_password="test_password2")

    test_user1 = (
        db.session.query(user.User).filter_by(email="test_email@email.com").one()
    )
    user_id = test_user1.id
    asin = "B076V9P58R"
    url = create_url(asin)
    track_asin(url, asin, user_id, config_class=TestingConfig)

    test_user2 = (
        db.session.query(user.User).filter_by(email="test2_email@email.com").one()
    )
    user_id2 = test_user2.id
    track_asin(url, asin, user_id2, config_class=TestingConfig)

    # Test if user 1 persists in DB
    assert db.session.query(user.User).filter_by(email="test_email@email.com").one()
    # Test if user 2 persists in DB
    assert db.session.query(user.User).filter_by(email="test2_email@email.com").one()
    # Test if there is exactly one item in DB
    assert db.session.query(item.Item).one()
    # Test that item is attached to user 1
    test_user1 = (
        db.session.query(user.User).filter_by(email="test_email@email.com").one()
    )
    assert (
        item.Item.query.join(
            users_items_association,
            (users_items_association.c.user_id == test_user1.id),
        )
        .filter(users_items_association.c.item_id == item.Item.id)
        .one()
    )
    # Test that item is attached to user 2
    test_user2 = (
        db.session.query(user.User).filter_by(email="test2_email@email.com").one()
    )
    assert (
        item.Item.query.join(
            users_items_association,
            (users_items_association.c.user_id == test_user2.id),
        )
        .filter(users_items_association.c.item_id == item.Item.id)
        .one()
    )
