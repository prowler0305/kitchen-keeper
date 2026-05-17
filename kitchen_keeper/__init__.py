from kitchen_keeper.extensions.database import db, migrate
from flask import Flask

from kitchen_keeper.blueprints import register_blueprints
from kitchen_keeper.config import Config
import kitchen_keeper.models

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database extension with app
    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)

    return app