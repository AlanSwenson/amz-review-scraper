"""Email Routes"""
from flask import url_for, redirect, Blueprint

email_blueprint = Blueprint(
    "email",
    __name__,
    static_url_path="static",
    static_folder="static",
    template_folder="templates",
)


@email_blueprint.route("/", methods=["POST", "GET"])
def root():
    """Route for email/ forwarding to signup/"""
    return redirect(url_for("signup.index"))
