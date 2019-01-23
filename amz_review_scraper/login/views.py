from flask import redirect, render_template, url_for, Blueprint, flash, request
from flask_login import login_user, current_user

from amz_review_scraper import bcrypt
from amz_review_scraper.login.forms import LoginForm
from amz_review_scraper.models.user import User

login_blueprint = Blueprint(
    "login",
    __name__,
    static_url_path="static",
    static_folder="static",
    template_folder="templates",
)


def log_user_in(form):
    user = User.query.filter_by(email=form.email.data.lower()).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("track.index"))

    else:
        flash("Login Unsuccessful. Please check email and password", "danger")
        return None


@login_blueprint.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("track.index"))
    form = LoginForm()

    if form.validate_on_submit():
        result = log_user_in(form)
        if result is not None:
            return result

    return render_template("login/index.html", title="Login", form=form)
