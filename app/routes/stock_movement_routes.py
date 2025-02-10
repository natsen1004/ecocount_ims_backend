from flask import Blueprint, request, abort, make_response
from ..models.stock_movement import StockMovement
from ..models.products import Products
from ..models.user import User
from ..models.reports import Reports
from datetime import datetime
from ..db import db
from app.services.notification_service import send_notification

bp= Blueprint("stock_movement_bp", __name__, url_prefix="/stock_movement")

@bp.post("")
def create_stock_movement():
    data = request.get_json()
    print("Incoming Data from Frontend:", data)

    product_name = data.get("product_name")
    if not product_name:
        abort(make_response({"error": "Product name is required"}, 400))

    product = Products.query.filter_by(name=product_name).first()
    if not product:
        abort(make_response({"error": "Product not found"}, 404))

    user = User.query.get(data.get("user_id"))
    if not user:
        abort(make_response({"error": "User not found"}, 404))

    timestamp = data.get("timestamp") or datetime.utcnow().isoformat()
    new_quantity = data.get("new_quantity")
    quantity_change = data.get("quantity_change")

    product.quantity = new_quantity

    stock_movement = StockMovement(
        product_id=product.id,
        user_id=user.id,
        product_name=product_name,
        sku=data.get("sku"),
        quantity_change=quantity_change,
        new_quantity=new_quantity,
        reason=data.get("reason"),
        timestamp=timestamp
    )
    db.session.add(stock_movement)

    report = Reports.query.filter_by(product_id=product.id, user_id=user.id).first()
    if report:
        report.quantity_sold += abs(quantity_change)  
    else:
        report = Reports(
            product_id=product.id,
            user_id=user.id,
            quantity_sold=abs(quantity_change) if quantity_change > 0 else 0  
        )
        db.session.add(report)

    db.session.commit()

    message = f"Stock movement for {product.name}: {quantity_change} units. New Quantity: {new_quantity}."
    send_notification(user.id, message, db.session, "Stock Movement", product.id)

    return {"stock_movement": stock_movement.to_dict(), "report": report.to_dict()}, 201



@bp.get("/<stock_movement_id>")
def get_stock_movement(stock_movement_id):
    stock_movement = StockMovement.query.get(stock_movement_id)
    
    if not stock_movement:
        abort(make_response({"error": f"Stock movement ID {stock_movement_id} not found"}, 404))

    return {"stock_movement": stock_movement.to_dict()}, 200

