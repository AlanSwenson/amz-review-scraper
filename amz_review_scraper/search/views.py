from flask import redirect, render_template, url_for, Blueprint

search_blueprint = Blueprint("search", __name__, template_folder="templates")


@search_blueprint.route("/")
def index():
    return redirect(url_for("search"))
