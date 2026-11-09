import warnings

from flask import current_app
from flask_wtf import FlaskForm
from PIL import Image, UnidentifiedImageError
from wtforms import (
    DecimalField,
    FileField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    Optional,
    ValidationError,
)


class CategoryForm(FlaskForm):
    name = StringField(
        "Nom de la catégorie",
        filters=[lambda value: value.strip() if value is not None else value],
        validators=[DataRequired(), Length(max=100)],
    )
    description = TextAreaField(
        "Description",
        filters=[lambda value: value.strip() if value is not None else value],
        validators=[Optional(), Length(max=2000)],
    )
    submit = SubmitField("Enregistrer")


def validate_product_image(form, field):
    upload = field.data
    if upload is None or not upload.filename:
        return

    extension = upload.filename.rsplit(".", 1)[-1].lower()
    expected_formats = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        "webp": "WEBP",
    }
    if "." not in upload.filename or extension not in expected_formats:
        raise ValidationError("Formats acceptés : JPG, PNG ou WEBP.")

    stream = upload.stream
    stream.seek(0, 2)
    size = stream.tell()
    stream.seek(0)
    if size > current_app.config["MAX_PRODUCT_IMAGE_SIZE"]:
        raise ValidationError("L’image ne doit pas dépasser 5 Mo.")

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(stream) as image:
                image_format = image.format
                width, height = image.size
                if width * height > 20_000_000:
                    raise ValidationError(
                        "La résolution de l’image ne doit pas dépasser 20 mégapixels."
                    )
                image.verify()
    except (
        UnidentifiedImageError,
        OSError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ) as error:
        raise ValidationError("Le fichier envoyé n’est pas une image valide.") from error
    finally:
        stream.seek(0)

    if image_format != expected_formats[extension]:
        raise ValidationError("L’extension du fichier ne correspond pas à son format.")


class ProductForm(FlaskForm):
    name = StringField(
        "Nom du produit",
        filters=[lambda value: value.strip() if value is not None else value],
        validators=[DataRequired(), Length(max=150)],
    )
    description = TextAreaField(
        "Description",
        filters=[lambda value: value.strip() if value is not None else value],
        validators=[Optional(), Length(max=5000)],
    )
    price = DecimalField(
        "Prix (€)",
        places=2,
        validators=[DataRequired(), NumberRange(min=0.01, max=99999999.99)],
    )
    stock = IntegerField(
        "Quantité en stock",
        validators=[DataRequired(), NumberRange(min=0, max=2147483647)],
    )
    image = StringField(
        "URL de l’image (facultative)",
        filters=[lambda value: value.strip() if value is not None else value],
        validators=[Optional(), Length(max=255)],
    )
    image_file = FileField(
        "Importer une image",
        validators=[validate_product_image],
    )
    category_id = SelectField(
        "Catégorie",
        coerce=int,
        validators=[DataRequired()],
    )
    submit = SubmitField("Enregistrer le produit")
