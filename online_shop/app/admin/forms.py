from flask_wtf import FlaskForm
from wtforms import (
    DecimalField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional


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
        "URL ou chemin de l’image",
        filters=[lambda value: value.strip() if value is not None else value],
        validators=[Optional(), Length(max=255)],
    )
    category_id = SelectField(
        "Catégorie",
        coerce=int,
        validators=[DataRequired()],
    )
    submit = SubmitField("Enregistrer le produit")
