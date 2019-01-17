from flask import redirect, render_template, url_for, Blueprint, flash
from flask_login import current_user

import amz_review_scraper.models.item as item

results_blueprint = Blueprint(
    "results",
    __name__,
    static_url_path="/static",
    static_folder="./static",
    template_folder="templates",
)


@results_blueprint.route("/")
def index():
    res = item.get_results(user_id=current_user.id)
    return render_template("results/index.html", title="Results", res=res)
