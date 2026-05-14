import importlib
import pkgutil

from flask import Flask
import kitchen_keeper.views


def register_blueprints(app: Flask) -> None:
    package = kitchen_keeper.views

    for module_info in pkgutil.iter_modules(package.__path__):
        module_name = f"{package.__name__}.{module_info.name}"
        module = importlib.import_module(module_name)

        register = getattr(module, "register", None)

        if callable(register):
            register(app)