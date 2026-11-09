from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


def _strip_value(value):
    return value.strip() if value is not None else value


class ContactForm(FlaskForm):
    name = StringField(
        "Nom",
        filters=[_strip_value],
        validators=[DataRequired(), Length(max=100)],
    )
    email = EmailField(
        "Adresse e-mail",
        filters=[_strip_value],
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    subject = StringField(
        "Sujet",
        filters=[_strip_value],
        validators=[DataRequired(), Length(max=150)],
    )
    message = TextAreaField(
        "Message",
        filters=[_strip_value],
        validators=[DataRequired(), Length(min=10, max=5000)],
    )
    submit = SubmitField("Envoyer le message")
