from amz_review_scraper import db
import amz_review_scraper.models.user as user


def create_test_user(email, plain_password):
    test_user = user.User(email=email, password=plain_password)
    db.session.add(test_user)
    db.session.commit()
