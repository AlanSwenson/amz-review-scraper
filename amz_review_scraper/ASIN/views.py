from flask import redirect, render_template, url_for, Blueprint

import amz_review_scraper.models.review as review
import amz_review_scraper.models.item as item


ASIN_blueprint = Blueprint(
    "ASIN",
    __name__,
    static_url_path="static",
    static_folder="static",
    template_folder="templates",
)


@ASIN_blueprint.route("/<asin>", methods=["POST", "GET"])
def index(asin):
    asin = asin.upper()
    title = "Reviews for " + asin
    revs = review.get_results(asin)
    product = item.get_name(asin)
    return render_template("ASIN/index.html", title=title, revs=revs, product=product)
