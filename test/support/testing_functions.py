from amz_review_scraper import db, bcrypt
import amz_review_scraper.models.user as user


def create_test_user(email, plain_password):
    hashed_password = bcrypt.generate_password_hash(plain_password).decode("utf-8")
    test_user = user.User(email=email, password=hashed_password)
    db.session.add(test_user)
    db.session.commit()
