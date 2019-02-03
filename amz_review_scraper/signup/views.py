from flask import render_template, url_for, flash, redirect, request, Blueprint

from flask_jwt_extended import get_jwt_identity, jwt_optional

from amz_review_scraper import db, bcrypt
from amz_review_scraper.models.user import User
from amz_review_scraper.signup.forms import RegistrationForm


signup_blueprint = Blueprint(
    "signup",
    __name__,
    static_url_path="static",
    static_folder="static",
    template_folder="templates",
)


@signup_blueprint.route("/", methods=["GET", "POST"])
@jwt_optional
def index():
    if get_jwt_identity() is not None:
        return redirect(url_for("track.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("login.index"))
    return render_template("signup/index.html", title="Sign Up", form=form)
