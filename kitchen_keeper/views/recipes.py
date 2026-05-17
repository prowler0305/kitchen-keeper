from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask.views import MethodView
from kitchen_keeper.extensions.database import db
from kitchen_keeper.models import Recipe
from sqlalchemy import select

recipe_bp = Blueprint("recipes", __name__, url_prefix="/recipes")
TEMPLATE_PREFIX = "recipes/"

RECIPE_FORM_FIELDS = {
    "title": str,
    "description": str,
    "category": str,
    "prep_time": str,
    "cook_time": str,
    "servings": int,
    "tags": str,
}

SAMPLE_RECIPES = [
    {
        "id": 1,
        "title": "Chicken Parmesan",
        "description": "Crispy chicken with marinara and melted cheese.",
        "category": "Dinner",
        "prep_time": "20 min",
        "cook_time": "30 min",
        "servings": 4,
        "tags": ["Family Favorite", "Comfort Food"],
        "ingredients": [
            "2 chicken breasts",
            "1 cup breadcrumbs",
            "1 cup marinara sauce",
            "1 cup shredded mozzarella",
            "1/2 cup grated parmesan"
        ],
        "instructions": [
            "Preheat oven to 400°F",
            "Bread the chicken and pan-fry until golder",
            "Top with marinara and cheese.",
            "Bake until cheese is melted and check is cooked through."
        ]
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

def apply_recipe_form(recipe: Recipe) -> None:
    for field, converter in RECIPE_FORM_FIELDS.items():
        value = request.form.get(field)

        if value == "":
            value = None

        if value is not None and converter is int:
            value = int(value)

        setattr(recipe, field, value)

class RecipeListView(MethodView):
    def get(self):
        recipes = db.session.execute(select(Recipe)).scalars().all()

        return render_template(
            f"{TEMPLATE_PREFIX}list.html",
            recipes=recipes
        )


class RecipeDetailView(MethodView):
    def get(self, recipe_id: int):
        recipe = db.session.get(Recipe, recipe_id)
        if recipe is None:
            abort(404)
        return render_template(f"{TEMPLATE_PREFIX}detail.html", recipe=recipe)


class RecipeCreateView(MethodView):
    def get(self):
        """
        Render the create html that includes the POST form.
        :return:
        """
        return render_template(f"{TEMPLATE_PREFIX}create.html", recipe=None)

    def post(self):
        """
        Handle the add recipe form
        :return:
        """
        recipe = Recipe()
        apply_recipe_form(recipe)

        db.session.add(recipe)
        db.session.commit()

        return redirect(url_for("recipes.detail", recipe_id=recipe.id))

class RecipeEditView(MethodView):
    def get(self, recipe_id: int):
        recipe = Recipe.query.get_or_404(recipe_id)
        return render_template(f"{TEMPLATE_PREFIX}edit.html", recipe=recipe)

    def post(self, recipe_id: int):
        """
        Update a recipe.
        :return:
        """
        recipe = db.get_or_404(Recipe, recipe_id)
        apply_recipe_form(recipe)

        db.session.commit()
        return redirect(url_for("recipes.detail", recipe_id=recipe.id))


class RecipeDeleteView(MethodView):
    def post(self, recipe_id: int):
        recipe = db.get_or_404(Recipe, recipe_id)

        db.session.delete(recipe)
        db.session.commit()

        return redirect(url_for("recipes.list"))

recipe_bp.add_url_rule("/", view_func=RecipeListView.as_view("list"))
recipe_bp.add_url_rule("/new", view_func=RecipeCreateView.as_view("create"))
recipe_bp.add_url_rule("/<int:recipe_id>", view_func=RecipeDetailView.as_view("detail"))
recipe_bp.add_url_rule("/<int:recipe_id>/edit", view_func=RecipeEditView.as_view("edit"))
recipe_bp.add_url_rule("/<int:recipe_id>/delete", view_func=RecipeDeleteView.as_view("delete"))

def register(app) -> None:
    app.register_blueprint(recipe_bp)