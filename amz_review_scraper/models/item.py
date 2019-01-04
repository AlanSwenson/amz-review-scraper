from amz_review_scraper import db
from datetime import datetime

from amz_review_scraper.models.users_items_association import users_items_association


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

    def update_last_scraped(self):
        db.session.query(Item).filter_by(asin=self.asin).update(
            {"last_scraped": datetime.utcnow()}
        )


def get_results(asin=None, user_id=None):
    if asin is not None:
        return Item.query.filter_by(asin=asin).first()
    elif user_id is not None:
        return Item.query.join(
            users_items_association, (users_items_association.c.user_id == user_id)
        ).filter(users_items_association.c.item_id == Item.id)
    else:
        return Item.query.all()
