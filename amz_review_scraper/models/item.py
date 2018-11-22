from app import db


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    customer_reviews_count = db.Column(db.Integer)
    asin = db.Column(db.String(10), unique=True)
    reviews = db.relationship("Review", backref="owner", lazy=True)

    def save(self):
        db.session.add(self)

    def check(self):
        return db.session.query(Item).filter_by(asin=self.asin).scalar()
