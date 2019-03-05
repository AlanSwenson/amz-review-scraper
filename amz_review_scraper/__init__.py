import os

from flask import Flask, redirect, url_for, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_s3 import FlaskS3
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_jwt_extended import (
    JWTManager,
    jwt_optional,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_refresh_token_required,
    create_access_token,
    set_access_cookies,
)

from amz_review_scraper.config import DevelopmentConfig, ProductionConfig


db = SQLAlchemy()
migrate = Migrate()
s3 = FlaskS3()
bcrypt = Bcrypt()
jwt = JWTManager()
moment = Moment()
mail = Mail()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__, static_url_path="/static")
    if "ZAPPA" in os.environ and os.environ["ZAPPA"] == "True":
        config_class = ProductionConfig
    app.config.from_object(config_class)
    app.jinja_env.globals["jwt_user"] = get_jwt_identity

    with app.app_context():
        initialize_extensions(app)
        register_blueprints(app)

    @app.route("/", methods=["POST", "GET"])
    @jwt_optional
    def root():
        if get_jwt_identity() is not None:
            return redirect(url_for("track.index"))
        return redirect(url_for("signup.index"))

    @app.route("/logout")
    def logout():
        resp = redirect(url_for("login.index"))
        unset_jwt_cookies(resp)
        return resp, 302

    @app.route("/refresh", methods=["GET"])
    @jwt_refresh_token_required
    def refresh():
        # Create the new access token
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        response = redirect(url_for("track.index"))
        response.set_cookie("access_token", value=access_token)
        # Set the JWT access cookie in the response
        set_access_cookies(response, access_token)
        return response, 302

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html", title="404")

    # Redirect to Login when trying to access a protected route
    @jwt.unauthorized_loader
    def unauthorized_loader(self):
        return redirect(url_for("login.index"))

    @jwt.expired_token_loader
    def expired_token_loader():
        return redirect(url_for("logout"))

    return app


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    s3.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    moment.init_app(app)
    mail.init_app(app)


def register_blueprints(app):
    from amz_review_scraper.track.views import track_blueprint
    from amz_review_scraper.results.views import results_blueprint
    from amz_review_scraper.login.views import login_blueprint
    from amz_review_scraper.signup.views import signup_blueprint
    from amz_review_scraper.ASIN.views import ASIN_blueprint
    from amz_review_scraper.email.views import email_blueprint
    from amz_review_scraper.user.views import user_blueprint
    from amz_review_scraper.admin.views import admin_blueprint

    app.register_blueprint(track_blueprint, url_prefix="/track")
    app.register_blueprint(results_blueprint, url_prefix="/results")
    app.register_blueprint(login_blueprint, url_prefix="/login")
    app.register_blueprint(signup_blueprint, url_prefix="/signup")
    app.register_blueprint(ASIN_blueprint, url_prefix="/ASIN")
    app.register_blueprint(email_blueprint, url_prefix="/email")
    app.register_blueprint(user_blueprint, url_prefix="/user")
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
