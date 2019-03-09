from flask import redirect, render_template, url_for, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

import amz_review_scraper.models.item as item
from amz_review_scraper.urls import create_url
from amz_review_scraper.tasks import track_asin
from amz_review_scraper import db
from amz_review_scraper.models.users_items_association import users_items_association
from amz_review_scraper.models.item import Item
from amz_review_scraper.models.user import get_current_user


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
    if get_jwt_identity():
        user_id = get_jwt_identity()
        url = create_url(asin)
        track_asin(url, asin, user_id)
        return redirect(url_for("results.index"))


@results_blueprint.route("/stop_tracking/<asin>", methods=["POST", "GET"])
@jwt_required
def stop_tracking(asin):
    if get_jwt_identity():
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
