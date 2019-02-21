from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask import current_app as app
from flask_jwt_extended import get_jwt_identity, jwt_optional, jwt_required
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime

from amz_review_scraper import db, bcrypt
from amz_review_scraper.email import send_email
from amz_review_scraper.models.user import User
from amz_review_scraper.signup.forms import RegistrationForm
import amz_review_scraper.models.user as user_methods


signup_blueprint = Blueprint(
    "signup",
    __name__,
    static_url_path="static",
    static_folder="static",
    template_folder="templates",
)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
    except:
        return False
    return email


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


@signup_blueprint.route("/confirm/<token>")
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash("The confirmation link is invalid or has expired.", "danger")
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash("Account already confirmed. Please login.", "success")
    else:
        user.confirmed = True
        user.confirmed_on = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")

    return redirect(url_for("login.index"))


@signup_blueprint.route("/unconfirmed", methods=["GET", "POST"])
def unconfirmed():
    return render_template("signup/unconfirmed.html")


@signup_blueprint.route("/resend")
@jwt_required
def resend_confirmation():
    current_user = user_methods.get_current_user()
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for("signup.confirm_email", token=token, _external=True)
    html = render_template("signup/activate.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash("A new confirmation email has been sent.", "success")
    return redirect(url_for("signup.unconfirmed"))
