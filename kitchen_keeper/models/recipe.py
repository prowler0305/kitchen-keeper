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
