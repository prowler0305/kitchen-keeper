from flask import Blueprint, render_template
from flask.views import MethodView

main_bp = Blueprint("main", __name__)


class HomeView(MethodView):
    def get(self):
        return render_template("index.html")

main_bp.add_url_rule("/", view_func=HomeView.as_view("home"))

def register(app):
    app.register_blueprint(main_bp)