from pathlib import Path
from uuid import uuid4

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def save_recipe_image(file: FileStorage) -> str | None:
    """
    Handle image upload for recipes
    :param file:
    :return:
    """
    # Check file exits
    if not file or not file.filename:
        return None

    # Makes filename secure
    original_filename = secure_filename(file.filename)

    # Validate the extension
    if "." not in original_filename:
        raise ValueError("Unsupported image type.")

    extension = original_filename.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError("Unsupported image type.")

    # Generate unique filename
    filename = f"{uuid4().hex}.{extension}"

    # Create upload directory
    upload_dir = Path(current_app.config.get("RECIPE_IMAGE_UPLOAD_FOLDER"))
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Save the image file
    file.save(upload_dir / filename)

    # return the stored filename
    return filename

def delete_recipe_image(filename: str | None) -> None:
    if not filename:
        return

    image_path = Path(current_app.config.get("RECIPE_IMAGE_UPLOAD_FOLDER")) / filename

    try:
        image_path.unlink(missing_ok=True)
    except OSError:
        current_app.logger.exception(
            "Failed to delete recipe image",
            extra={"filename": filename},
        )