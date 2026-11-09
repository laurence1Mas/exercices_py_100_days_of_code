from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update

from app.extensions import db
from app.models import CartItem, Order, OrderItem, Product


cart = Blueprint("cart", __name__, url_prefix="/cart")


def _cart_items():
    return db.session.scalars(
        db.select(CartItem)
        .where(CartItem.user_id == current_user.id)
        .order_by(CartItem.id)
    ).all()


@cart.get("/")
@login_required
def index():
    items = _cart_items()
    total = sum(item.product.price * item.quantity for item in items)
    checkout_available = bool(items) and all(
        item.quantity > 0 and item.quantity <= item.product.stock
        for item in items
    )
    return render_template(
        "cart.html",
        items=items,
        total=total,
        checkout_available=checkout_available,
    )


@cart.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    items = _cart_items()
    if not items:
        flash("Votre panier est vide.", "error")
        return redirect(url_for("cart.index"))

    if request.method == "POST":
        if any(
            item.quantity < 1
            or item.quantity > item.product.stock
            for item in items
        ):
            flash(
                "Le stock d’un article a changé. Vérifiez votre panier avant de réessayer.",
                "error",
            )
            return redirect(url_for("cart.index"))

        total = sum(item.product.price * item.quantity for item in items)
        order = Order(
            user_id=current_user.id,
            total_amount=round(total, 2),
            status="PROCESSING",
            payment_status="PAID",
        )
        db.session.add(order)

        for item in items:
            deleted_item = db.session.execute(
                sqlalchemy_delete(CartItem).where(
                    CartItem.id == item.id,
                    CartItem.user_id == current_user.id,
                    CartItem.quantity == item.quantity,
                )
            )
            if deleted_item.rowcount != 1:
                db.session.rollback()
                flash(
                    "Votre panier a changé pendant la validation. "
                    "Vérifiez-le avant de réessayer.",
                    "error",
                )
                return redirect(url_for("cart.index"))

            result = db.session.execute(
                sqlalchemy_update(Product)
                .where(
                    Product.id == item.product_id,
                    Product.stock >= item.quantity,
                )
                .values(stock=Product.stock - item.quantity)
            )
            if result.rowcount != 1:
                db.session.rollback()
                flash(
                    "Le stock d’un article vient d’être épuisé. "
                    "Votre commande n’a pas été créée.",
                    "error",
                )
                return redirect(url_for("cart.index"))

            order.items.append(
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.product.price,
                )
            )

        db.session.commit()
        flash(
            "Paiement simulé accepté. Votre commande est confirmée.",
            "success",
        )
        return redirect(url_for("orders.detail", order_id=order.id))

    total = sum(item.product.price * item.quantity for item in items)
    available = all(
        item.quantity > 0 and item.quantity <= item.product.stock
        for item in items
    )
    return render_template(
        "checkout.html",
        items=items,
        total=total,
        available=available,
    )


@cart.post("/add/<int:product_id>")
@login_required
def add(product_id):
    product = db.session.get(Product, product_id)
    if product is None:
        flash("Ce produit n’est plus disponible.", "error")
        return redirect(url_for("shop"))

    try:
        quantity = int(request.form.get("quantity", "1"))
    except ValueError:
        flash("La quantité demandée est invalide.", "error")
        return redirect(url_for("product_detail", product_id=product.id))

    if quantity < 1:
        flash("La quantité doit être au moins égale à 1.", "error")
        return redirect(url_for("product_detail", product_id=product.id))
    if quantity > product.stock:
        flash("La quantité demandée dépasse le stock disponible.", "error")
        return redirect(url_for("product_detail", product_id=product.id))

    item = db.session.scalar(
        db.select(CartItem).where(
            CartItem.user_id == current_user.id,
            CartItem.product_id == product.id,
        )
    )
    new_quantity = quantity + (item.quantity if item else 0)
    if new_quantity > product.stock:
        flash(
            "La quantité totale dépasse le stock disponible.",
            "error",
        )
        return redirect(url_for("product_detail", product_id=product.id))

    if item is None:
        item = CartItem(
            user_id=current_user.id,
            product_id=product.id,
            quantity=quantity,
        )
        db.session.add(item)
    else:
        item.quantity = new_quantity

    db.session.commit()
    flash(f"{product.name} a été ajouté à votre panier.", "success")
    return redirect(url_for("cart.index"))


@cart.post("/<int:item_id>/update")
@login_required
def update(item_id):
    item = db.session.scalar(
        db.select(CartItem).where(
            CartItem.id == item_id,
            CartItem.user_id == current_user.id,
        )
    )
    if item is None:
        flash("Cet article n’existe pas dans votre panier.", "error")
        return redirect(url_for("cart.index"))

    try:
        quantity = int(request.form.get("quantity", ""))
    except ValueError:
        flash("La quantité demandée est invalide.", "error")
        return redirect(url_for("cart.index"))

    if quantity < 1:
        flash("La quantité doit être au moins égale à 1.", "error")
    elif quantity > item.product.stock:
        flash("La quantité demandée dépasse le stock disponible.", "error")
    else:
        item.quantity = quantity
        db.session.commit()
        flash("La quantité a été mise à jour.", "success")
    return redirect(url_for("cart.index"))


@cart.post("/<int:item_id>/remove")
@login_required
def remove(item_id):
    item = db.session.scalar(
        db.select(CartItem).where(
            CartItem.id == item_id,
            CartItem.user_id == current_user.id,
        )
    )
    if item is None:
        flash("Cet article n’existe pas dans votre panier.", "error")
        return redirect(url_for("cart.index"))

    db.session.delete(item)
    db.session.commit()
    flash("L’article a été retiré de votre panier.", "success")
    return redirect(url_for("cart.index"))