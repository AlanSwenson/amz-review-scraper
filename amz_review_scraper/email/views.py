from flask import render_template, url_for, redirect, Blueprint
from flask import current_app as app
from flask_jwt_extended import get_jwt_identity, jwt_optional, jwt_required

email_blueprint = Blueprint(
    "email",
    __name__,
    static_url_path="static",
    static_folder="static",
    template_folder="templates",
)


@email_blueprint.route("/", methods=["POST", "GET"])
def root():
    return redirect(url_for("signup.index"))
