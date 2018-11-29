from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from amz_review_scraper.config import Config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    migrate = Migrate()

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        csrf.init_app(app)
        register_blueprints(app)

    @app.route("/", methods=["POST", "GET"])
    def root():
        return redirect(url_for("track.index"))

    return app


def register_blueprints(app):
    from amz_review_scraper.track.views import track_blueprint
    from amz_review_scraper.results.views import results_blueprint

    app.register_blueprint(track_blueprint, url_prefix="/track")
    app.register_blueprint(results_blueprint, url_prefix="/results")
