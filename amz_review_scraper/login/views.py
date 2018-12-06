from flask import redirect, render_template, url_for, Blueprint, flash

from amz_review_scraper.login.forms import Login_form

login_blueprint = Blueprint(
    "login",
    __name__,
    static_url_path="static",
    static_folder="static",
    template_folder="templates",
)


@login_blueprint.route("/", methods=["GET", "POST"])
def index():
    form = Login_form()
    return render_template("login/index.html", title="Login", form=form)
