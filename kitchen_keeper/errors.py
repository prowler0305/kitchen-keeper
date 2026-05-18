from flask import flash, redirect, request, url_for, Flask
from flask_wtf.csrf import CSRFError


def handle_csrf_error(error):
    flash("Your session expired or the form could not be verified. Please try again.",
          "danger"
    )

    return redirect(
        request.referrer or url_for("recipes.list")
    )

def register_error_handlers(app: Flask) -> None:
    app.register_error_handler(CSRFError, handle_csrf_error)