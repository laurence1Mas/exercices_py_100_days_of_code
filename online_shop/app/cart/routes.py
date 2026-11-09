from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import CartItem, Product


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
    return render_template("cart.html", items=items, total=total)


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