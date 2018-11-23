from app import db
from datetime import datetime


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(10), unique=True)
    name = db.Column(db.String)
    customer_reviews_count = db.Column(db.Integer)
    reviews = db.relationship("Review", backref="owner", lazy=True)
    last_scraped = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def save(self):
        db.session.add(self)

    def check(self):
        return db.session.query(Item).filter_by(asin=self.asin).scalar()
