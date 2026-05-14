from flask import Flask

from kitchen_keeper.blueprints import register_blueprints
from kitchen_keeper.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_blueprints(app)

    return app