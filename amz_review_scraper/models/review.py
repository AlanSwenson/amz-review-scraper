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
    if asin is not None:
        if review is not None:
            return (
                db.session.query(Review)
                .filter_by(asin=asin)
                .filter_by(review=review)
                .first()
            )
        return Review.query.filter_by(asin=asin)
    return Review.query.all()
