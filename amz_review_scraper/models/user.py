from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from amz_review_scraper import db, login_manager
from amz_review_scraper.models.users_items_association import users_items_association


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items = db.relationship("Item", secondary=users_items_association, backref="user")

    def save(self):
        db.session.add(self)
