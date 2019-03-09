from flask import redirect, render_template, url_for, Blueprint

from flask_jwt_extended import jwt_required, get_jwt_identity

from amz_review_scraper.track.forms import Asin_search_form
from amz_review_scraper.urls import create_url
from amz_review_scraper.tasks import track_asin
from amz_review_scraper.decorators import check_confirmed


track_blueprint = Blueprint(
    "track",
    __name__,
    static_url_path="static",
    static_folder="static",
    template_folder="templates",
)


@track_blueprint.route("/", methods=["POST", "GET"])
@jwt_required
@check_confirmed
def index():
    form = Asin_search_form()
    if form.validate_on_submit() and get_jwt_identity():
        user_id = get_jwt_identity()
        asin = form.asin.data
        url = create_url(asin)
        track_asin(url, asin, user_id)

        return redirect(url_for("results.index"))

    return render_template("track/index.html", title="Track", form=form)
