from kitchen_keeper.extensions.marshmallow import ma
from marshmallow import validate, fields, pre_load


class RecipeFormSchema(ma.Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = fields.String(load_default="")
    category = fields.String(load_default="")
    prep_time = fields.String(load_default="")
    cook_time = fields.String(load_default="")
    servings = fields.Integer(allow_none=True, load_default=None)
    tags = fields.String(load_default="")

    ingredients = fields.List(
        fields.String(validate=validate.Length(min=1)),
        required=True,
        validate=validate.Length(min=1))

    instructions = fields.List(
        fields.String(validate=validate.Length(min=1)),
        required=True,
        validate=validate.Length(min=1))


    @pre_load
    def clean_input(self, data, **kwargs):
        data = dict(data)

        for field_name, field in self.fields.items():
            form_value = data.get(field_name)

            if isinstance(field, fields.List):
                data[field_name] = [item.strip() for item in form_value or [] if item.strip()]
            elif isinstance(form_value, str):
                data[field_name] = form_value.strip()

        return data