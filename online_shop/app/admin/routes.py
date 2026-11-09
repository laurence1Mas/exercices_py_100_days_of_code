from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.admin.forms import CategoryForm, ProductForm
from app.extensions import db
from app.models import (
    CartItem,
    Category,
    ContactMessage,
    Order,
    OrderItem,
    Product,
    User,
)


admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.before_request
def require_admin_role():
    if current_user.is_authenticated and current_user.role != "ADMIN":
        abort(403)


@admin.get("/")
@login_required
def dashboard():
    product_count, customer_count, order_count, pending_count, paid_revenue = (
        _dashboard_metrics()
    )
    recent_orders = db.session.scalars(
        db.select(Order).order_by(
            Order.created_at.desc(),
            Order.id.desc(),
        ).limit(5)
    ).all()

    return render_template(
        "admin/dashboard.html",
        product_count=product_count,
        customer_count=customer_count,
        order_count=order_count,
        pending_count=pending_count,
        paid_revenue=paid_revenue,
        recent_orders=recent_orders,
    )


@admin.get("/products")
@login_required
def products():
    return _render_products_page()


@admin.post("/products/new")
@login_required
def create_product():
    form = _product_form()
    if form.validate_on_submit():
        product = _product_from_form(form)
        db.session.add(product)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash(
                "Le produit n’a pas pu être enregistré. "
                "Vérifiez la catégorie choisie.",
                "error",
            )
            return _render_products_page(
                product_form=form,
                active_modal="create",
            )
        else:
            flash("Le produit a été créé.", "success")
            return redirect(url_for("admin.products"))

    return _render_products_page(product_form=form, active_modal="create")


@admin.post("/products/<int:product_id>/edit")
@login_required
def edit_product(product_id):
    product = db.get_or_404(Product, product_id)
    form = _product_form(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        product.price = float(form.price.data)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash(
                "Le produit n’a pas pu être modifié. "
                "Vérifiez la catégorie choisie.",
                "error",
            )
            return _render_products_page(
                product_form=form,
                active_modal="edit",
                editing_product=product,
            )
        else:
            flash("Le produit a été modifié.", "success")
            return redirect(url_for("admin.products"))

    return _render_products_page(
        product_form=form,
        active_modal="edit",
        editing_product=product,
    )


@admin.post("/products/<int:product_id>/delete")
@login_required
def delete_product(product_id):
    product = db.get_or_404(Product, product_id)
    has_cart_references = db.session.scalar(
        db.select(CartItem.id).where(CartItem.product_id == product.id).limit(1)
    )
    has_order_references = db.session.scalar(
        db.select(OrderItem.id).where(OrderItem.product_id == product.id).limit(1)
    )
    if has_cart_references or has_order_references:
        flash(
            "Ce produit est utilisé dans un panier ou une commande et ne peut pas être supprimé.",
            "error",
        )
    else:
        db.session.delete(product)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash(
                "Le produit n’a pas pu être supprimé en raison de références "
                "existantes.",
                "error",
            )
        else:
            flash("Le produit a été supprimé.", "success")
    return redirect(url_for("admin.products"))


def _product_form(obj=None):
    form = ProductForm(obj=obj)
    form.category_id.choices = [
        (category.id, category.name)
        for category in db.session.scalars(
            db.select(Category).order_by(Category.name)
        ).all()
    ]
    return form


def _product_from_form(form):
    return Product(
        name=form.name.data,
        description=form.description.data or None,
        price=float(form.price.data),
        stock=form.stock.data,
        image=form.image.data or None,
        category_id=form.category_id.data,
    )


def _render_products_page(
    product_form=None,
    active_modal=None,
    editing_product=None,
):
    products = db.session.scalars(
        db.select(Product).order_by(Product.name, Product.id)
    ).all()
    categories = db.session.scalars(
        db.select(Category).order_by(Category.name)
    ).all()
    return render_template(
        "admin/products.html",
        products=products,
        categories=categories,
        product_form=product_form if product_form is not None else _product_form(),
        active_modal=active_modal,
        editing_product=editing_product,
    )


@admin.get("/categories")
@login_required
def categories():
    categories = db.session.scalars(
        db.select(Category)
        .order_by(Category.name)
    ).all()
    return render_template("admin/categories.html", categories=categories)


@admin.route("/categories/new", methods=["GET", "POST"])
@login_required
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        if _category_name_exists(form.name.data):
            form.name.errors.append("Une catégorie porte déjà ce nom.")
        else:
            category = Category(
                name=form.name.data,
                description=form.description.data or None,
            )
            db.session.add(category)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                form.name.errors.append("Une catégorie porte déjà ce nom.")
            else:
                flash("La catégorie a été créée.", "success")
                return redirect(url_for("admin.categories"))

    return render_template(
        "admin/category_form.html",
        form=form,
        page_title="Créer une catégorie",
        category=None,
    )


@admin.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
@login_required
def edit_category(category_id):
    category = db.get_or_404(Category, category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        if _category_name_exists(form.name.data, exclude_id=category.id):
            form.name.errors.append("Une catégorie porte déjà ce nom.")
        else:
            category.name = form.name.data
            category.description = form.description.data or None
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                form.name.errors.append("Une catégorie porte déjà ce nom.")
            else:
                flash("La catégorie a été modifiée.", "success")
                return redirect(url_for("admin.categories"))

    return render_template(
        "admin/category_form.html",
        form=form,
        page_title="Modifier une catégorie",
        category=category,
    )


@admin.post("/categories/<int:category_id>/delete")
@login_required
def delete_category(category_id):
    category = db.get_or_404(Category, category_id)
    if category.products:
        flash(
            "Cette catégorie contient des produits. "
            "Réaffectez-les avant de la supprimer.",
            "error",
        )
    else:
        db.session.delete(category)
        db.session.commit()
        flash("La catégorie a été supprimée.", "success")
    return redirect(url_for("admin.categories"))


@admin.get("/orders")
@login_required
def orders():
    orders = db.session.scalars(
        db.select(Order).order_by(
            Order.created_at.desc(),
            Order.id.desc(),
        )
    ).all()
    return render_template("admin/orders.html", orders=orders)


@admin.get("/messages")
@login_required
def messages():
    messages = db.session.scalars(
        db.select(ContactMessage).order_by(
            ContactMessage.created_at.desc(),
            ContactMessage.id.desc(),
        ).limit(100)
    ).all()
    return render_template("admin/messages.html", messages=messages)


@admin.get("/stock")
@login_required
def stock():
    products = db.session.scalars(
        db.select(Product).order_by(Product.stock, Product.name)
    ).all()
    total_stock = db.session.scalar(
        db.select(func.coalesce(func.sum(Product.stock), 0))
    ) or 0
    return render_template(
        "admin/stock.html",
        products=products,
        total_stock=total_stock,
    )


@admin.get("/statistics")
@login_required
def statistics():
    product_count, customer_count, order_count, pending_count, paid_revenue = (
        _dashboard_metrics()
    )
    return render_template(
        "admin/statistics.html",
        product_count=product_count,
        customer_count=customer_count,
        order_count=order_count,
        pending_count=pending_count,
        paid_revenue=paid_revenue,
    )


def _dashboard_metrics():
    product_count = db.session.scalar(
        db.select(func.count(Product.id))
    ) or 0
    customer_count = db.session.scalar(
        db.select(func.count(User.id)).where(User.role == "CUSTOMER")
    ) or 0
    order_count = db.session.scalar(
        db.select(func.count(Order.id))
    ) or 0
    pending_count = db.session.scalar(
        db.select(func.count(Order.id)).where(Order.status == "PENDING")
    ) or 0
    paid_revenue = db.session.scalar(
        db.select(func.coalesce(func.sum(Order.total_amount), 0)).where(
            Order.payment_status == "PAID"
        )
    ) or 0
    return product_count, customer_count, order_count, pending_count, paid_revenue


def _category_name_exists(name, exclude_id=None):
    query = db.select(Category.id, Category.name)
    if exclude_id is not None:
        query = query.where(Category.id != exclude_id)
    normalized_name = name.casefold()
    return any(
        existing_name.casefold() == normalized_name
        for _, existing_name in db.session.execute(query)
    )