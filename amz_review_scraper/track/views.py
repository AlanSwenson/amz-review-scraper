from flask import redirect, render_template, url_for, Blueprint, flash
from flask_login import login_required

from amz_review_scraper.track.forms import Asin_search_form
import amz_review_scraper.urls as urls
import amz_review_scraper.get_soup as get_soup
import amz_review_scraper.amzscraper as amazon


track_blueprint = Blueprint(
    "track",
    __name__,
    static_url_path="static",
    static_folder="static",
    template_folder="templates",
)


@track_blueprint.route("/", methods=["POST", "GET"])
@login_required
def index():
    form = Asin_search_form()
    if form.validate_on_submit():
        asin = form.asin.data
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
    return render_template("track/index.html", title="Track", form=form)
