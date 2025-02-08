from flask import Blueprint, request, abort, make_response
from ..models.reports import Reports
from ..db import db
from ..models.products import Products
from ..models.stock_movement import StockMovement
from app.routes.route_utilities import validate_model

bp = Blueprint("reports_bp", __name__, url_prefix="/reports")  

@bp.post("")
def create_report():
    """Creates a report based on product sales."""
    data = request.get_json()
    product_id = data.get("product_id")
    user_id = data.get("user_id")
    quantity_sold = data.get("quantity_sold", 0)

    product = validate_model(Products, product_id)
    if not product:
        abort(make_response({"message": f"Product ID {product_id} not found"}, 404))

    new_report = Reports(
        product_id=product_id,
        user_id=user_id,
        quantity_sold=quantity_sold
    )
    db.session.add(new_report)
    db.session.commit()

    return {"report": new_report.to_dict()}, 201 

@bp.get("")
def get_all_reports():
    user_id = request.args.get("user_id")
    if not user_id:
        return {"error": "User ID is required to fetch reports"}, 400

    reports = Reports.query.filter_by(user_id=user_id).all()
    
    report_data = []
    for report in reports:
        product = Products.query.get(report.product_id)
        stock_movements = StockMovement.query.filter_by(product_id=report.product_id, user_id=user_id).all()

        report_data.append({
            "product_id": report.product_id,
            "product_name": product.name if product else "Unknown",
            "total_quantity_sold": report.quantity_sold, 
            "stock_movements": [
                {
                    "timestamp": movement.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "quantity_change": movement.quantity_change,
                    "new_quantity": movement.new_quantity,
                }
                for movement in stock_movements
            ],
        })

    return report_data, 200



