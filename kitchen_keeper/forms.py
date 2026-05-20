from types import SimpleNamespace

from marshmallow import fields


def load_form_with_schema(schema, form):
    """
    Load and validate submitted HTML form data using a Marshmallow schema.

    The schema is used as the source of truth for which fields should be read
    from the form. Scalar fields are read with form.get(), while list fields are
    read with form.getlist() so repeated HTML inputs can be validated as normal
    Python lists.

    :param schema: Marshmallow schema instance used to define and validate fields.
    :param form: Flask/Werkzeug form MultiDict from request.form.
    :return: Validated and normalized data returned by schema.load().
    :raises marshmallow.ValidationError: If submitted form data fails validation.
    """
    data = {}

    for field_name, field in schema.fields.items():
        if isinstance(field, fields.List):
            data[field_name] = form.getlist(field_name)
        else:
            data[field_name] = form.get(field_name)

    return schema.load(data)

def build_form_view_model(schema, form, **extra_attrs):
    """
    Build a temporary object-shaped view model from submitted HTML form data.

    This is used when validation fails and the form needs to be re-rendered with
    the user's submitted values preserved. The returned object mimics the shape
    expected by the Jinja templates, allowing templates to continue using
    attribute access such as recipe.title, recipe.ingredients, and ingredient.text.

    The schema is used as the source of truth for which fields should be read
    from the form. List fields are converted into SimpleNamespace objects with a
    text attribute so they match the shape of RecipeIngredient and
    RecipeInstruction objects used during normal edit rendering.

    Additional attributes, such as id for edit forms, may be supplied with
    extra_attrs.

    :param schema: Marshmallow schema instance used to define expected fields.
    :param form: Flask/Werkzeug form MultiDict from request.form.
    :param extra_attrs: Optional attributes to add to the returned view model.
    :return: SimpleNamespace object suitable for rendering the form template.
    """
    data = {}

    for field_name, field in schema.fields.items():
        if isinstance(field, fields.List):
            data[field_name] = [SimpleNamespace(text=value) for value in form.getlist(field_name)]
        else:
            data[field_name] = form.get(field_name, "")

    data.update(extra_attrs)

    return SimpleNamespace(**data)