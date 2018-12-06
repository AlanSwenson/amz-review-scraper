from flask import redirect, render_template, url_for, Blueprint, flash


login_blueprint = Blueprint(
    "login",
    __name__,
    static_url_path="static",
    static_folder="static",
    template_folder="templates",
)


@login_blueprint.route("/")
def index():
    return render_template("login/index.html", title="Login")
