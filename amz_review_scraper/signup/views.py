from flask import redirect, render_template, url_for, Blueprint, flash

signup_blueprint = Blueprint(
    "signup",
    __name__,
    static_url_path="static",
    static_folder="static",
    template_folder="templates",
)


@signup_blueprint.route("/", methods=["GET", "POST"])
def index():
    # form = Register_form()
    return render_template("signup/index.html", title="Sign Up")
