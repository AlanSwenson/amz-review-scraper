from flask import redirect, render_template, url_for, Blueprint, flash
from amz_review_scraper.search.forms import Asin_search_form

search_blueprint = Blueprint(
    "search",
    __name__,
    static_url_path="/search/static",
    static_folder="./static",
    template_folder="templates",
)


@search_blueprint.route("/", methods=["POST", "GET"])
def index():
    form = Asin_search_form()
    if form.validate_on_submit():
        flash("Thanks!")
    return render_template("search/index.html", title="Search", form=form)
