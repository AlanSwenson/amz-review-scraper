import requests
import json


from flask import (
    redirect,
    render_template,
    url_for,
    Blueprint,
    flash,
    request,
    jsonify,
    current_app,
)
from flask_login import login_user, current_user
from flask_jwt_extended import (
    jwt_required,
    jwt_optional,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    set_refresh_cookies,
    set_access_cookies,
)

from amz_review_scraper import bcrypt
from amz_review_scraper.login.forms import LoginForm
from amz_review_scraper.models.user import User


login_blueprint = Blueprint(
    "login",
    __name__,
    static_url_path="static",
    static_folder="static",
    template_folder="templates",
)


def log_user_in(form):
    user = User.query.filter_by(email=form.email.data.lower()).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        user_id = {"user_id": str(user.id)}
        login_base = current_app.config["LOGIN_BASE_URL"]
        login_path_url = f"{login_base}/login/auth"
        auth_response = requests.post(url=login_path_url, json=user_id)
        response = redirect(url_for("track.index"))
        login_data_dict = json.loads(auth_response.text)
        response.set_cookie("access_token", value=login_data_dict.get("access_token"))
        response.set_cookie("refresh_token", value=login_data_dict.get("refresh_token"))
        set_access_cookies(response, login_data_dict.get("access_token"))
        set_refresh_cookies(response, login_data_dict.get("refresh_token"))
        return response
        # TODO: reinstate the next_page setup with JWT
        # next_page = request.args.get("next")
        # return redirect(next_page) if next_page else redirect(url_for("track.index"))
    else:
        flash("Login Unsuccessful. Please check email and password", "danger")
        return None


@login_blueprint.route("/auth", methods=["POST"])
def auth():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    user_id = request.json["user_id"]
    print("user_id: " + user_id)
    tokens = {
        "access_token": create_access_token(identity=user_id),
        "refresh_token": create_refresh_token(identity=user_id),
    }
    return jsonify(tokens), 200


@login_blueprint.route("/", methods=["GET", "POST"])
@jwt_optional
def index():
    if get_jwt_identity() is not None:
        print("No User")
        return redirect(url_for("track.index"))
    form = LoginForm()

    if form.validate_on_submit():
        result = log_user_in(form)
        if result is not None:
            return result

    return render_template("login/index.html", title="Login", form=form)
