def db_init():
    from amz_review_scraper import create_app, db

    app = create_app()
    app.app_context().push()

    from amz_review_scraper.models.users_items_association import (
        users_items_association,
    )
    from amz_review_scraper.models.user import User
    from amz_review_scraper.models.item import Item
    from amz_review_scraper.models.review import Review
    from amz_review_scraper.models.token_blacklist import TokenBlacklist

    db.create_all()


if __name__ == "__main__":
    db_init()
