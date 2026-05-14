from flask import Blueprint, render_template
from flask.views import MethodView

recipe_bp = Blueprint("recipes", __name__, url_prefix="/recipes")
TEMPLATE_PREFIX = "recipes/"

SAMPLE_RECIPES = [
    {
        "id": 1,
        "title": "Chicken Parmesan",
        "description": "Crispy chicken with marinara and melted cheese.",
        "category": "Dinner",
        "prep_time": "20 min",
        "cook_time": "30 min",
        "servings": 4,
    },
    {
        "id": 2,
        "title": "Banana Bread",
        "description": "A soft, sweet loaf for using ripe bananas.",
        "category": "Baking",
        "prep_time": "15 min",
        "cook_time": "55 min",
        "servings": 8,
    },
    {
        "id": 3,
        "title": "Creamy Tuscan Pasta",
        "description": "A rich garlic parmesan pasta with spinach and sun-dried tomatoes.",
        "category": "Pasta",
        "prep_time": "15 min",
        "cook_time": "25 min",
        "servings": 6,
    },
    {
        "id": 4,
        "title": "Classic Beef Tacos",
        "description": "Seasoned ground beef tacos with fresh toppings and shredded cheese.",
        "category": "Mexican",
        "prep_time": "10 min",
        "cook_time": "20 min",
        "servings": 4,
    },
]

class RecipeListView(MethodView):
    def get(self):
        return render_template(
            f"{TEMPLATE_PREFIX}list.html",
            recipes=SAMPLE_RECIPES
        )

class RecipeDetailView(MethodView):
    def get(self, recipe_id: int):
        return render_template(f"{TEMPLATE_PREFIX}detail.html")

class RecipeCreateView(MethodView):
    def get(self):
        return render_template(f"{TEMPLATE_PREFIX}create.html")

class RecipeEditView(MethodView):
    def get(self, recipe_id: int):
        return render_template(f"{TEMPLATE_PREFIX}edit.html")

recipe_bp.add_url_rule("/", view_func=RecipeListView.as_view("list"))
recipe_bp.add_url_rule("/new", view_func=RecipeCreateView.as_view("create"))
recipe_bp.add_url_rule("/<int:recipe_id>", view_func=RecipeDetailView.as_view("detail"))
recipe_bp.add_url_rule("/<int:recipe_id>/edit", view_func=RecipeEditView.as_view("edit"))

def register(app) -> None:
    app.register_blueprint(recipe_bp)