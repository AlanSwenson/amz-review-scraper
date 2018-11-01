from app import db


#db = SQLAlchemy(app)

class Items(db.Model):
    __tablename__ = "items"
    name = db.Column(db.String)
    customer_reviews_count = db.Column(db.Integer)
    asin = db.Column(db.String(10), primary_key=True)

class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(10), primary_key=True)
    review = db.Column(db.String)
