from flask import redirect, render_template, url_for, Blueprint, flash
from flask_login import current_user

import amz_review_scraper.models.item as item
import amz_review_scraper.urls as urls
import amz_review_scraper.get_soup as get_soup
import amz_review_scraper.amzscraper as amazon

results_blueprint = Blueprint(
    "results",
    __name__,
    static_url_path="/static",
    static_folder="./static",
    template_folder="templates",
)


@results_blueprint.route("/refresh_asin/<asin>", methods=["POST", "GET"])
def refresh_asin(asin):
    url = urls.create_url(asin)
    soup = get_soup.boil_soup(url, asin)
    if soup.status_code != None:
        flash(
            "ASIN returned Status Code: "
            + str(soup.status_code)
            + " Please check your ASIN and try Again"
        )
    else:
        amazon.scrape(soup, asin)
    return redirect(url_for("results.index"))


@results_blueprint.route("/")
def index():
    res = item.get_results(user_id=current_user.id)
    return render_template("results/index.html", title="Results", res=res)
