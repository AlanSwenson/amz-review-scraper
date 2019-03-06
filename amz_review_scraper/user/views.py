from datetime import datetime

from flask import render_template, url_for, flash, redirect, Blueprint
from flask_jwt_extended import jwt_required


from amz_review_scraper import db, bcrypt
from amz_review_scraper.email_functions import (
    send_email,
    generate_confirmation_token,
    confirm_token,
    send_reset_email,
)
from amz_review_scraper.models.user import User
from amz_review_scraper.signup.forms import ResetPasswordForm, RequestResetForm
import amz_review_scraper.models.user as user_methods

user_blueprint = Blueprint("user", __name__, template_folder="templates")


@user_blueprint.route("/confirm/<token>")
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


@user_blueprint.route("/unconfirmed", methods=["GET", "POST"])
def unconfirmed():
    return render_template("email/unconfirmed_email.html")


@user_blueprint.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            "An email has been sent with instructions to reset your password.", "info"
        )
        return redirect(url_for("login.index"))
    return render_template(
        "user/reset_password.html", title="Reset Password", form=form
    )


@user_blueprint.route("/resend")
@jwt_required
def resend_confirmation():
    current_user = user_methods.get_current_user()
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for("user.confirm_email", token=token, _external=True)
    html = render_template("user/activate.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash("A new confirmation email has been sent.", "success")
    return redirect(url_for("user.unconfirmed"))


@user_blueprint.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    try:
        email = confirm_token(token)
    except:
        flash("The password reset link is invalid or has expired.", "danger")
        return redirect(url_for("user.reset_request"))
    user = User.query.filter_by(email=email).first_or_404()

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You are now able to log in", "success")
        return redirect(url_for("login.index"))
    return render_template("user/reset_token.html", title="Reset Token", form=form)
