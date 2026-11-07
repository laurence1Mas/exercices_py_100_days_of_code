
from flask import Flask

from config import Config
from app.extensions import db, login_manager, csrf


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"

    # Importer les modèles pour les enregistrer auprès de SQLAlchemy
    from app import models

    # Créer les tables
    with app.app_context():
        db.create_all()

    return app
