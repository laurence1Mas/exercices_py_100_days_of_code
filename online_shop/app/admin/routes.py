import re
from pathlib import Path
from uuid import uuid4

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from PIL import Image, ImageOps
from sqlalchemy import func
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

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
from app.orders.statuses import (
    ORDER_STATUS_LABELS,
    ORDER_STATUS_TRANSITIONS,
    PAYMENT_STATUS_LABELS,
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
        order_status_labels=ORDER_STATUS_LABELS,
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
        try:
            uploaded_image = _store_product_image(form.image_file.data)
        except (OSError, ValueError):
            current_app.logger.exception("Unable to save uploaded product image")
            flash("L’image n’a pas pu être enregistrée. Réessayez.", "error")
            return _render_products_page(
                product_form=form,
                active_modal="create",
            )

        product = _product_from_form(form, uploaded_image=uploaded_image)
        db.session.add(product)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            if uploaded_image:
                _remove_uncommitted_product_image(uploaded_image)
            flash(
                "Le produit n’a pas pu être enregistré. "
                "Vérifiez la catégorie choisie.",
                "error",
            )
            return _render_products_page(
                product_form=form,
                active_modal="create",
            )
        except SQLAlchemyError:
            db.session.rollback()
            if uploaded_image:
                _remove_uncommitted_product_image(uploaded_image)
            raise
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
        old_image = product.image
        try:
            uploaded_image = _store_product_image(form.image_file.data)
        except (OSError, ValueError):
            current_app.logger.exception("Unable to save uploaded product image")
            flash("L’image n’a pas pu être enregistrée. Réessayez.", "error")
            return _render_products_page(
                product_form=form,
                active_modal="edit",
                editing_product=product,
            )

        form.populate_obj(product)
        product.price = float(form.price.data)
        if uploaded_image:
            product.image = uploaded_image
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            if uploaded_image:
                _remove_uncommitted_product_image(uploaded_image)
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
        except SQLAlchemyError:
            db.session.rollback()
            if uploaded_image:
                _remove_uncommitted_product_image(uploaded_image)
            raise
        else:
            if old_image != product.image:
                _remove_product_image_if_unused(old_image)
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
    image = product.image
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
            _remove_product_image_if_unused(image)
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


def _product_from_form(form, uploaded_image=None):
    return Product(
        name=form.name.data,
        description=form.description.data or None,
        price=float(form.price.data),
        stock=form.stock.data,
        image=uploaded_image or form.image.data or None,
        category_id=form.category_id.data,
    )


def _store_product_image(upload):
    if upload is None or not upload.filename:
        return None

    with Image.open(upload.stream) as image:
        image_format = image.format
        image = ImageOps.exif_transpose(image)
        if image_format == "JPEG" and image.mode not in ("RGB", "L"):
            image = image.convert("RGB")
        elif image_format == "WEBP" and image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA")

        extensions = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}
        extension = extensions[image_format]
        filename = f"{uuid4().hex}{extension}"
        upload_folder = Path(current_app.config["PRODUCT_UPLOAD_FOLDER"])
        upload_folder.mkdir(parents=True, exist_ok=True)
        image_path = upload_folder / filename
        try:
            save_options = {"quality": 90} if image_format in {"JPEG", "WEBP"} else {}
            if image_format == "PNG":
                save_options["optimize"] = True
            image.save(image_path, format=image_format, **save_options)
        except (OSError, ValueError):
            image_path.unlink(missing_ok=True)
            raise

    return url_for("static", filename=f"uploads/products/{filename}")


def _remove_product_image_if_unused(image_url):
    image_path = _product_image_path(image_url)
    if image_path is None:
        return
    still_used = db.session.scalar(
        db.select(Product.id).where(Product.image == image_url).limit(1)
    )
    if not still_used:
        _unlink_product_image(image_path)


def _remove_uncommitted_product_image(image_url):
    image_path = _product_image_path(image_url)
    if image_path is not None:
        _unlink_product_image(image_path)


def _product_image_path(image_url):
    prefix = url_for("static", filename="uploads/products/")
    if not image_url or not image_url.startswith(prefix):
        return None

    filename = image_url[len(prefix):]
    if not re.fullmatch(r"[0-9a-f]{32}\.(?:jpg|png|webp)", filename):
        return None
    return Path(current_app.config["PRODUCT_UPLOAD_FOLDER"]) / filename


def _unlink_product_image(image_path):
    try:
        image_path.unlink()
    except FileNotFoundError:
        return
    except OSError:
        current_app.logger.exception("Unable to remove unused product image")


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
    return render_template(
        "admin/orders.html",
        orders=orders,
        order_status_labels=ORDER_STATUS_LABELS,
        payment_status_labels=PAYMENT_STATUS_LABELS,
    )


@admin.get("/orders/<int:order_id>")
@login_required
def order_detail(order_id):
    order = db.get_or_404(Order, order_id)
    next_statuses = ORDER_STATUS_TRANSITIONS.get(order.status, ())
    return render_template(
        "admin/order_detail.html",
        order=order,
        next_statuses=next_statuses,
        order_status_labels=ORDER_STATUS_LABELS,
        payment_status_labels=PAYMENT_STATUS_LABELS,
    )


@admin.post("/orders/<int:order_id>/status")
@login_required
def update_order_status(order_id):
    order = db.get_or_404(Order, order_id)
    new_status = request.form.get("status", "")
    allowed_statuses = ORDER_STATUS_TRANSITIONS.get(order.status, ())
    if new_status not in allowed_statuses:
        flash("Cette transition de statut n’est pas autorisée.", "error")
        return redirect(url_for("admin.order_detail", order_id=order.id))

    current_status = order.status
    status_update = {"status": new_status}
    if new_status == "CANCELLED":
        if order.payment_status == "PAID":
            status_update["payment_status"] = "REFUNDED"
    updated_order = db.session.execute(
        update(Order)
        .where(
            Order.id == order.id,
            Order.status == current_status,
        )
        .values(**status_update)
    )
    if updated_order.rowcount != 1:
        db.session.rollback()
        flash(
            "La commande a déjà été mise à jour. Rechargez la page pour voir son état.",
            "error",
        )
        return redirect(url_for("admin.order_detail", order_id=order.id))

    if new_status == "CANCELLED":
        for item in order.items:
            db.session.execute(
                update(Product)
                .where(Product.id == item.product_id)
                .values(stock=Product.stock + item.quantity)
            )
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise

    flash(
        f"La commande #{order.id} est maintenant "
        f"{ORDER_STATUS_LABELS[new_status].lower()}.",
        "success",
    )
    return redirect(url_for("admin.order_detail", order_id=order.id))


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


@admin.get("/messages/<int:message_id>")
@login_required
def message_detail(message_id):
    message = db.get_or_404(ContactMessage, message_id)
    return render_template("admin/message_detail.html", message=message)


@admin.post("/messages/<int:message_id>/delete")
@login_required
def delete_message(message_id):
    message = db.get_or_404(ContactMessage, message_id)
    db.session.delete(message)
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise

    flash("Le message a été supprimé.", "success")
    return redirect(url_for("admin.messages"))


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
        db.select(func.count(Order.id)).where(
            Order.status.in_(("PENDING", "PROCESSING"))
        )
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