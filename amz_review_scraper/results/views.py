from flask import redirect, render_template, url_for, Blueprint, flash
from flask_jwt_extended import get_jwt_identity, jwt_required

import amz_review_scraper.models.item as item
import amz_review_scraper.urls as urls
import amz_review_scraper.get_soup as get_soup
import amz_review_scraper.amzscraper as amazon
from amz_review_scraper import db
from amz_review_scraper.models.users_items_association import users_items_association
from amz_review_scraper.models.item import Item
from amz_review_scraper.models.user import User, get_current_user


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


@results_blueprint.route("/stop_tracking/<asin>", methods=["POST", "GET"])
@jwt_required
def stop_tracking(asin):
    if get_jwt_identity() is not None:
        link_to_delete = (
            Item.query.join(
                users_items_association,
                (users_items_association.c.user_id == get_jwt_identity()),
            )
            .filter(users_items_association.c.item_id == Item.id)
            .filter(Item.asin == asin)
            .first()
        )
        user = get_current_user()
        link_to_delete.users.remove(user)
        db.session.commit()

    return redirect(url_for("results.index"))


@results_blueprint.route("/")
@jwt_required
def index():
    res = item.get_results(user_id=get_jwt_identity())
    return render_template("results/index.html", title="Results", res=res)
