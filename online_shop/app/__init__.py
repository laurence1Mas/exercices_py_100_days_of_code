
from flask import Flask, render_template

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
    from app.auth.routes import auth

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(models.User, user_id)

    # Créer les tables
    with app.app_context():
        db.create_all()

    app.register_blueprint(auth)

    @app.get("/")
    def home():
        return render_template("index.html")

    return app
