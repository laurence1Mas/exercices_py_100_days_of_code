from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    name = StringField(
        "Nom",
        validators=[DataRequired(), Length(max=100)]
    )
    email = StringField(
        "Adresse e-mail",
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    password = PasswordField(
        "Mot de passe",
        validators=[DataRequired(), Length(min=8)]
    )
    confirm_password = PasswordField(
        "Confirmer le mot de passe",
        validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Créer mon compte")


class LoginForm(FlaskForm):
    email = StringField(
        "Adresse e-mail",
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")