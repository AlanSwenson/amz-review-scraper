from datetime import datetime

from sqlalchemy.orm import relationship
from flask_jwt_extended import get_jwt_identity

from amz_review_scraper import db
from amz_review_scraper.models.users_items_association import users_items_association


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items = db.relationship("Item", secondary=users_items_association, backref="user")
    admin = db.Column(db.Boolean, nullable=True, default=False)
    confirmed = db.Column(db.Boolean, nullable=True, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def save(self):
        db.session.add(self)


def get_current_user():
    return User.query.filter_by(id=get_jwt_identity()).one_or_none()
