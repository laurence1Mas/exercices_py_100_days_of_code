from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


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
