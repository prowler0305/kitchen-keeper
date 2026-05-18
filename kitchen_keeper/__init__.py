import os

from kitchen_keeper.extensions.database import db, migrate
from flask import Flask

from kitchen_keeper.blueprints import register_blueprints
from kitchen_keeper.config import Config
import kitchen_keeper.models
from logging_config import configure_logging


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ.get("APP_ENV", "kitchen_keeper.config.DevelopmentConfig"))
    configure_logging(app)
    # Initialize database extension with app
    db.init_app(app)
    migrate.init_app(app, db)
    # Discovery and register all application blueprints.
    register_blueprints(app)

    return app