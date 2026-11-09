from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required
from sqlalchemy import func

from app.extensions import db
from app.models import Order, Product, User


admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.before_request
def require_admin_role():
    if current_user.is_authenticated and current_user.role != "ADMIN":
        abort(403)


@admin.get("/")
@login_required
def dashboard():
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