from datetime import datetime

from flask import render_template, url_for, flash, redirect, Blueprint
from flask_jwt_extended import jwt_optional

from amz_review_scraper import db, bcrypt
from amz_review_scraper.email_functions import send_email, generate_confirmation_token
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
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            email=form.email.data.lower(),
            password=hashed_password,
            confirmed=False,
            date_created=datetime.utcnow(),
        )
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for("signup.confirm_email", token=token, _external=True)
        html = render_template("signup/activate.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)

        flash("A confirmation email has been sent via email.", "success")
        return redirect(url_for("login.index"))
    return render_template("signup/index.html", title="Sign Up", form=form)

