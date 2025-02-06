from flask import Blueprint, request, abort, make_response
from ..models.stock_movement import StockMovement
from ..models.products import Products
from ..db import db
from datetime import datetime
from app.routes.route_utilities import validate_model
from app.services.notification_service import check_and_create_stock_alert

bp= Blueprint("stock_movement_bp", __name__, url_prefix="/stock_movement")

@bp.post("")
def create_stock_movement():
    data = request.get_json()
    product = Products.query.get(data.get("product_id"))
    if not product:
        abort(make_response({"error": "Product not found"}, 404))

    stock_movement = StockMovement.from_dict(data)
    db.session.add(stock_movement)
    db.session.commit()
    return {"stock_movement": stock_movement.to_dict()}, 201

@bp.get("")
def get_stock_movements():
    stock_movements = StockMovement.query.all()
    return [sm.to_dict() for sm in stock_movements], 200
