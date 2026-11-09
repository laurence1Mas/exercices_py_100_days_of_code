from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Order


orders = Blueprint("orders", __name__, url_prefix="/orders")


@orders.get("/")
@login_required
def index():
    user_orders = db.session.scalars(
        db.select(Order)
        .where(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc(), Order.id.desc())
    ).all()
    return render_template("orders.html", orders=user_orders)


@orders.get("/<int:order_id>")
@login_required
def detail(order_id):
    order = db.session.scalar(
        db.select(Order).where(
            Order.id == order_id,
            Order.user_id == current_user.id,
        )
    )
    if order is None:
        abort(404)
    return render_template("orders/detail.html", order=order)