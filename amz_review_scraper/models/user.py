"""User model and associated functions"""

from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask_jwt_extended import get_jwt_identity

from amz_review_scraper import db, bcrypt
from amz_review_scraper.models.users_items_association import users_items_association


class User(db.Model):
    """Model for storing Users"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column("password", db.String(128))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items = db.relationship("Item", secondary=users_items_association, backref="user")
    admin = db.Column(db.Boolean, nullable=True, default=False)
    confirmed = db.Column(db.Boolean, nullable=True, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        """
        sets password

        Parameters
        ----------
        plaintext : string
            user password in plaintext
        """
        self._password = bcrypt.generate_password_hash(plaintext).decode("utf-8")

    @hybrid_method
    def is_correct_password(self, plaintext):
        """
        checks if password matches the password in db

        Parameters
        ----------
        plaintext : string
            user password in plaintext

        Returns
        -------
        bool :
            True if password matches
        """
        return bcrypt.check_password_hash(self.password, plaintext)

    def save(self):
        """Saves user to DB"""
        db.session.add(self)


def get_current_user():
    """
    gets the current user that is logged in

    Returns
    -------
    User or None
    """
    return User.query.filter_by(id=get_jwt_identity()).one_or_none()
