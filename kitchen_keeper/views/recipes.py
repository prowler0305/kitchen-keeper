from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask.views import MethodView
from kitchen_keeper.extensions.database import db
from kitchen_keeper.forms import load_form_with_schema, build_form_view_model
from kitchen_keeper.models import Recipe, RecipeIngredient, RecipeInstruction
from kitchen_keeper.schemas.recipe import RecipeFormSchema
from marshmallow import ValidationError
from sqlalchemy import select, inspect

recipe_bp = Blueprint("recipes", __name__, url_prefix="/recipes")
TEMPLATE_PREFIX = "recipes/"

def apply_recipe_form(recipe: Recipe, data) -> Recipe:
    """
    Transfer the validated form data into a Recipe object.
    :param recipe:
    :param data:
    :return:
    """
    # Use SQLAlchemy inspect to retrieve the Recipe object definition to
    # access the metadata of thr ORM model definition
    mapper = inspect(type(recipe))
    # Get the relationships list object.
    relationships = mapper.relationships

    for field_name, value in data.items():
        if field_name in relationships:
            child_model = relationships[field_name].mapper.class_

            setattr(
                recipe,
                field_name,
                [
                    child_model(
                        position=index,
                        text=text)
                    for index, text in enumerate(value, start=1)
                ]
            )
        else:
            setattr(recipe, field_name, value)

    return recipe

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
        return render_template(
            f"{TEMPLATE_PREFIX}create.html",
            recipe=None,
            errors={}
        )

    def post(self):
        """
        Handle the add recipe form
        :return:
        """
        schema = RecipeFormSchema()
        try:
            validated_data = load_form_with_schema(schema, request.form)
        except ValidationError as error:
            return render_template(
                f"{TEMPLATE_PREFIX}create.html",
                recipe=build_form_view_model(schema, request.form),
                errors=error.messages
            )

        recipe = Recipe()
        apply_recipe_form(recipe, validated_data)

        db.session.add(recipe)
        db.session.commit()
        flash("Recipe created successfully!", "success")
        return redirect(url_for("recipes.detail", recipe_id=recipe.id))

class RecipeEditView(MethodView):
    def get(self, recipe_id: int):
        recipe = db.get_or_404(Recipe, recipe_id)
        return render_template(
            f"{TEMPLATE_PREFIX}edit.html",
            recipe=recipe,
            errors={}
        )

    def post(self, recipe_id: int):
        """
        Update a recipe.
        :return:
        """
        recipe = db.get_or_404(Recipe, recipe_id)

        schema = RecipeFormSchema()
        try:
            validated_data = load_form_with_schema(schema, request.form)
        except ValidationError as error:
            # Re-render existing edit template
            return render_template(
                f"{TEMPLATE_PREFIX}edit.html",
                recipe=build_form_view_model(schema, request.form, id=recipe.id),
                errors=error.messages,
            )

        apply_recipe_form(recipe=recipe, data=validated_data)

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