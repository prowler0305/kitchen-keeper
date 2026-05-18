from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask.views import MethodView
from kitchen_keeper.extensions.database import db
from kitchen_keeper.models import Recipe, RecipeIngredient, RecipeInstruction
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

def apply_recipe_form(recipe: Recipe) -> None:
    for field, converter in RECIPE_FORM_FIELDS.items():
        value = request.form.get(field)

        if value == "":
            value = None

        if value is not None and converter is int:
            value = int(value)

        setattr(recipe, field, value)

    recipe.ingredients = [
        RecipeIngredient(position=index, text=value.strip())
        for index, value in enumerate(request.form.getlist("ingredients[]"), start=1)
        if value.strip()
    ]

    recipe.instructions = [
        RecipeInstruction(position=index, text=value.strip())
        for index, value in enumerate(request.form.getlist("instructions[]"), start=1)
        if value.strip()
    ]


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
        flash("Recipe created successfully!", "success")
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
        flash("Recipe updated successfully!", "success")
        return redirect(url_for("recipes.detail", recipe_id=recipe.id))


class RecipeDeleteView(MethodView):
    def post(self, recipe_id: int):
        recipe = db.get_or_404(Recipe, recipe_id)

        db.session.delete(recipe)
        db.session.commit()
        flash("Recipe deleted successfully!", "success")
        return redirect(url_for("recipes.list"))

recipe_bp.add_url_rule("/", view_func=RecipeListView.as_view("list"))
recipe_bp.add_url_rule("/new", view_func=RecipeCreateView.as_view("create"))
recipe_bp.add_url_rule("/<int:recipe_id>", view_func=RecipeDetailView.as_view("detail"))
recipe_bp.add_url_rule("/<int:recipe_id>/edit", view_func=RecipeEditView.as_view("edit"))
recipe_bp.add_url_rule("/<int:recipe_id>/delete", view_func=RecipeDeleteView.as_view("delete"))

def register(app) -> None:
    app.register_blueprint(recipe_bp)