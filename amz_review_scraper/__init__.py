from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from amz_review_scraper.config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    migrate = Migrate(app, db)

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        register_blueprints(app)

    @app.route("/")
    def root():
        return redirect(url_for("index"))

    return app


def register_blueprints(app):
    from amz_review_scraper.search.views import search_blueprint

    app.register_blueprint(search_blueprint, url_prefix="/search")
