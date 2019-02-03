from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from flask_jwt_extended import get_jwt_identity

from amz_review_scraper import db
from amz_review_scraper.models.users_items_association import users_items_association


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items = db.relationship("Item", secondary=users_items_association, backref="user")

    def save(self):
        db.session.add(self)


def get_current_user():
    return User.query.filter_by(id=get_jwt_identity()).one_or_none()
