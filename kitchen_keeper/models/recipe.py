from kitchen_keeper.extensions.database import db
from sqlalchemy.orm import Mapped, mapped_column


class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    prep_time = db.Column(db.String(50))
    cook_time = db.Column(db.String(50))
    servings = db.Column(db.Integer)
    tags = db.Column(db.String(50))

    ingredients = db.relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan",
        order_by="RecipeIngredient.position",
    )
    instructions = db.relationship(
        "RecipeInstruction",
        back_populates="recipe",
        cascade="all, delete-orphan",
        order_by="RecipeInstruction.position",
    )

    image_filename = db.Column(db.String(255), nullable=True)


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(500), nullable=False)

    recipe = db.relationship("Recipe", back_populates="ingredients")


class RecipeInstruction(db.Model):
    __tablename__ = 'recipe_instructions'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(500), nullable=False)

    recipe = db.relationship("Recipe", back_populates="instructions")
