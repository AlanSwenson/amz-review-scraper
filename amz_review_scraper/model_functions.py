def save_to_db():
    try:
        db.session.commit()
    except Exception as e:
        print(f"An Error Occurred While Saving to DB: {e}")
        db.session.rollback()
        raise
    finally:
        db.session.close()


def db_error(warning, e):
    print(f"An Error Occured While Saving {warning} to DB: {e}")
    db.session.rollback()


# Initialize the DB
if __name__ == "__main__":

    from amz_review_scraper import create_app, db

    app = create_app()
    app.app_context().push()

    from amz_review_scraper.models.users_items_association import (
        users_items_association,
    )
    from amz_review_scraper.models.user import User
    from amz_review_scraper.models.item import Item
    from amz_review_scraper.models.review import Review

    db.create_all()
else:
    from amz_review_scraper import db
