from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from amz_review_scraper.config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    migrate = Migrate()

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        register_blueprints(app)

    @app.route("/")
    def root():
        return redirect(url_for("search.index"))

    return app


def register_blueprints(app):
    from amz_review_scraper.search.views import search_blueprint

    app.register_blueprint(search_blueprint, url_prefix="/search")
