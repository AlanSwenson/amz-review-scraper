from flask import redirect, render_template, url_for, Blueprint, flash


results_blueprint = Blueprint(
    "results",
    __name__,
    static_url_path="/static",
    static_folder="./static",
    template_folder="templates",
)


@results_blueprint.route("/")
def index():
    return render_template("results/index.html", title="Results")
