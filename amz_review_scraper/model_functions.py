from app import db


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
def create_db():
    db.create_all()
