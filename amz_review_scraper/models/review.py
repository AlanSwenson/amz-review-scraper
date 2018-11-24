# from flask import current_app

from amz_review_scraper import db


class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(10))
    review = db.Column(db.String)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))

    def save(self):
        db.session.add(self)

    def check(self):
        return (
            db.session.query(Review)
            .filter_by(asin=self.asin)
            .filter_by(review=self.review)
            .scalar()
        )
