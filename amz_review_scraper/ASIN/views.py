from flask import redirect, render_template, url_for, Blueprint

import amz_review_scraper.models.review as review

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
    query = review.Review.query.filter_by(asin=asin).first_or_404()
    title = "Reviews for " + asin
    revs = review.get_results()
    return render_template("ASIN/index.html", title=title, revs=revs)
