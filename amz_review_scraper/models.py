from app import db

# Maybe change this to Item?
class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    customer_reviews_count = db.Column(db.Integer)
    asin = db.Column(db.String(10), unique=True)
    reviews = db.relationship("Review", backref="owner", lazy=True)

    def save(self):
        db.session.add(self)


class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(10))
    review = db.Column(db.String)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))

    def save(self):
        db.session.add(self)


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
