import os

from kitchen_keeper.errors import register_error_handlers
from kitchen_keeper.extensions.csrf import csrf
from kitchen_keeper.extensions.database import db, migrate
from flask import Flask

from kitchen_keeper.blueprints import register_blueprints
# While looking unused is needed for flask-migrate and SQLAlchemy to see table models
import kitchen_keeper.models
from kitchen_keeper.extensions.marshmallow import ma
from kitchen_keeper.logging_config import configure_logging


def create_app():
    app = Flask(__name__)

    app.config.from_object(
        os.environ.get(
            "APP_ENV",
            "kitchen_keeper.config.DevelopmentConfig"
        )
    )

    configure_logging(app)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    ma.init_app(app)

    # Discovery and register all application blueprints.
    register_blueprints(app)
    # Register error handlers
    register_error_handlers(app)

    return app