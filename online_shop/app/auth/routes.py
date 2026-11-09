from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.auth.forms import LoginForm, RegisterForm
from app.models import CartItem, Order, User


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.profile"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        existing_user = db.session.scalar(
            db.select(User).where(func.lower(User.email) == email)
        )
        if existing_user is not None:
            form.email.errors.append("Cette adresse e-mail est déjà utilisée.")
            return render_template("auth/register.html", form=form)

        user = User(
            name=form.name.data.strip(),
            email=email,
            password=generate_password_hash(form.password.data),
            role="CUSTOMER",
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Votre compte a été créé avec succès.", "success")
        return redirect(url_for("auth.profile"))

    return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.profile"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = db.session.scalar(
            db.select(User).where(func.lower(User.email) == email)
        )
        if user is None or not check_password_hash(user.password, form.password.data):
            flash("Adresse e-mail ou mot de passe incorrect.", "error")
            return render_template("auth/login.html", form=form)

        login_user(user)
        flash("Vous êtes connecté.", "success")
        if user.role == "ADMIN":
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("auth.profile"))

    return render_template("auth/login.html", form=form)


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "success")
    return redirect(url_for("auth.login"))


@auth.route("/profile")
@login_required
def profile():
    order_count = db.session.scalar(
        db.select(func.count(Order.id)).where(Order.user_id == current_user.id)
    ) or 0
    cart_item_count = db.session.scalar(
        db.select(func.coalesce(func.sum(CartItem.quantity), 0)).where(
            CartItem.user_id == current_user.id
        )
    ) or 0
    recent_orders = db.session.scalars(
        db.select(Order)
        .where(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc(), Order.id.desc())
        .limit(3)
    ).all()
    return render_template(
        "auth/profile.html",
        order_count=order_count,
        cart_item_count=cart_item_count,
        recent_orders=recent_orders,
    )