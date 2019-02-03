from flask import redirect, render_template, url_for, Blueprint, flash

import amz_review_scraper.models.item as item
import amz_review_scraper.urls as urls
import amz_review_scraper.get_soup as get_soup
import amz_review_scraper.amzscraper as amazon

from flask_jwt_extended import get_jwt_identity, jwt_required

results_blueprint = Blueprint(
    "results",
    __name__,
    static_url_path="/static",
    static_folder="./static",
    template_folder="templates",
)


@results_blueprint.route("/refresh_asin/<asin>", methods=["POST", "GET"])
@jwt_required
def refresh_asin(asin):
    if get_jwt_identity() is not None:
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
@jwt_required
def index():
    res = item.get_results(user_id=get_jwt_identity())
    return render_template("results/index.html", title="Results", res=res)
