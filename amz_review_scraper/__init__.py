from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_s3 import FlaskS3
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from amz_review_scraper.config import Config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
s3 = FlaskS3()
bcrypt = Bcrypt()
login_manager = LoginManager()
# login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        csrf.init_app(app)
        s3.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        register_blueprints(app)

    @app.route("/", methods=["POST", "GET"])
    def root():
        return redirect(url_for("track.index"))

    return app


def register_blueprints(app):
    from amz_review_scraper.track.views import track_blueprint
    from amz_review_scraper.results.views import results_blueprint
    from amz_review_scraper.login.views import login_blueprint
    from amz_review_scraper.signup.views import signup_blueprint

    app.register_blueprint(track_blueprint, url_prefix="/track")
    app.register_blueprint(results_blueprint, url_prefix="/results")
    app.register_blueprint(login_blueprint, url_prefix="/login")
    app.register_blueprint(signup_blueprint, url_prefix="/signup")
