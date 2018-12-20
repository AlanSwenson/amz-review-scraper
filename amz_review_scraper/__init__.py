from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_s3 import FlaskS3
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, logout_user

from amz_review_scraper.config import Config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
s3 = FlaskS3()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "login.index"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)

    with app.app_context():
        initialize_extensions(app)
        register_blueprints(app)

    @app.route("/", methods=["POST", "GET"])
    def root():
        if current_user.is_authenticated:
            return redirect(url_for("track.index"))
        return redirect(url_for("signup.index"))

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("login.index"))

    return app


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    s3.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    from amz_review_scraper.track.views import track_blueprint
    from amz_review_scraper.results.views import results_blueprint
    from amz_review_scraper.login.views import login_blueprint
    from amz_review_scraper.signup.views import signup_blueprint
    from amz_review_scraper.ASIN.views import ASIN_blueprint

    app.register_blueprint(track_blueprint, url_prefix="/track")
    app.register_blueprint(results_blueprint, url_prefix="/results")
    app.register_blueprint(login_blueprint, url_prefix="/login")
    app.register_blueprint(signup_blueprint, url_prefix="/signup")
    app.register_blueprint(ASIN_blueprint, url_prefix="/ASIN")
