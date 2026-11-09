from getpass import getpass

from email_validator import EmailNotValidError, validate_email
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import User


def main() -> int:
    app = create_app()

    email_input = input("Adresse e-mail de l’administrateur : ").strip()
    try:
        email = validate_email(
            email_input,
            check_deliverability=False,
        ).normalized.lower()
    except EmailNotValidError as error:
        print(f"Adresse e-mail invalide : {error}")
        return 1

    password = getpass("Mot de passe (12 caractères minimum) : ")
    if len(password) < 12:
        print("Le mot de passe doit contenir au moins 12 caractères.")
        return 1

    confirmation = getpass("Confirmez le mot de passe : ")
    if password != confirmation:
        print("Les mots de passe ne correspondent pas.")
        return 1

    with app.app_context():
        existing_user = db.session.scalar(
            db.select(User).where(func.lower(User.email) == email)
        )
        if existing_user is not None:
            if existing_user.role == "ADMIN":
                print("Un compte administrateur utilise déjà cette adresse.")
                return 0
            print(
                "Cette adresse appartient déjà à un compte client. "
                "Aucun changement n’a été effectué."
            )
            return 1

        admin = User(
            name=email.split("@", 1)[0],
            email=email,
            password=generate_password_hash(password),
            role="ADMIN",
        )
        db.session.add(admin)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print(
                "Un compte utilise déjà cette adresse. "
                "Aucun nouvel administrateur n’a été créé."
            )
            return 1

    print(f"Compte administrateur créé pour {email}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
