from app import db


#db = SQLAlchemy(app)


# Maybe change this to Item?
class Items(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    customer_reviews_count = db.Column(db.Integer)
    asin = db.Column(db.String(10), unique=True)
    reviews = db.relationship('Review', backref='owner', lazy=True)

class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(10))
    review = db.Column(db.String)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
