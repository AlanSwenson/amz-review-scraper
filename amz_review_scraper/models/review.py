from sqlalchemy.dialects.postgresql import insert

from amz_review_scraper import db


class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(10))
    review = db.Column(db.String)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))


def save(self):
    db.session.add(self)


def get_results(asin=None, review=None):
    try:
        if asin and review:
            return (
                db.session.query(Review)
                .filter_by(asin=asin)
                .filter_by(review=review)
                .first()
            )
        elif asin:
            return Review.query.filter_by(asin=asin)
        return Review.query.all()
    except Exception as e:
        print(f"An Error Occurred While Retrieving Reviews from DB: {e}")
        raise
        return None
