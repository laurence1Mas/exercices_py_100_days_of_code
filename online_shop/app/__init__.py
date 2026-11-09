
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import func, or_

from config import Config
from app.extensions import db, login_manager, csrf
from app.models import Category, ContactMessage, Product, User


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
    from app.cart.routes import cart
    from app.contact.forms import ContactForm
    from app.orders.routes import orders

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(models.User, user_id)

    # Créer les tables
    with app.app_context():
        db.create_all()

    app.register_blueprint(auth)
    app.register_blueprint(cart)
    app.register_blueprint(orders)
    from app.admin.routes import admin

    app.register_blueprint(admin)

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/univers")
    def univers():
        return render_template("univers.html")

    @app.get("/contact")
    @app.post("/contact")
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            db.session.add(
                ContactMessage(
                    name=form.name.data,
                    email=form.email.data,
                    subject=form.subject.data,
                    message=form.message.data,
                )
            )
            db.session.commit()
            flash(
                "Votre message a bien été enregistré. Merci de nous avoir contactés.",
                "success",
            )
            return redirect(url_for("contact"))

        if request.method == "GET" and current_user.is_authenticated:
            form.name.data = current_user.name
            form.email.data = current_user.email

        return render_template("contact.html", form=form)

    @app.get("/shop")
    def shop():
        """
        Affiche la page de la boutique avec les produits filtrés par catégorie et par recherche."""
        categories = db.session.scalars(
            db.select(Category).order_by(Category.name)
        ).all()
        selected_category = request.args.get("category", type=int)
        search_query = request.args.get("q", "").strip()[:80]
        product_query = db.select(Product).order_by(Product.name)

        if selected_category is not None:
            product_query = product_query.where(
                Product.category_id == selected_category
            )
        if search_query:
            search_pattern = f"%{search_query}%"
            product_query = product_query.where(
                or_(
                    Product.name.ilike(search_pattern),
                    Product.description.ilike(search_pattern),
                )
            )

        products = db.session.scalars(product_query).all()
        return render_template(
            "shop.html",
            categories=categories,
            products=products,
            search_query=search_query,
            selected_category=selected_category,
        )

    @app.get("/shop/<int:product_id>")
    def product_detail(product_id):
        product = db.session.get(Product, product_id)
        if product is None:
            abort(404)
        return render_template("product_detail.html", product=product)

    return app
