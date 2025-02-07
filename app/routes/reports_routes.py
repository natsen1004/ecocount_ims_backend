from flask import Blueprint, request, abort, make_response
from ..models.reports import Reports
from ..db import db
from ..models.stock_movement import StockMovement
from app.routes.route_utilities import validate_model

bp = Blueprint("report_bp", __name__, url_prefix="/reports")

@bp.get("")
def get_all_reports():
    user_id = request.args.get("user_id")
    if not user_id:
        return {"error": "User ID is required to fetch reports"}, 400
    stock_movements = StockMovement.query.filter_by(user_id=user_id).all()

    if not stock_movements:
        return [], 200 

    report_data = {}
    for movement in stock_movements:
        product_id = movement.product_id

        if product_id not in report_data:
            report_data[product_id] = {
                "product_id": product_id,
                "product_name": movement.product_name,
                "total_quantity_sold": 0,
                "stock_movements": []
            }

        if movement.quantity_change < 0: 
            report_data[product_id]["total_quantity_sold"] += abs(movement.quantity_change)

        report_data[product_id]["stock_movements"].append({
            "timestamp": movement.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "quantity_change": movement.quantity_change,
            "new_quantity": movement.new_quantity,
        })
    reports = list(report_data.values())

    return reports, 200


@bp.get("")
def get_all_reports():
    user_id = request.args.get("user_id")
    if not user_id:
        return {"error": "User ID is required to fetch reports"}, 400

    reports = Reports.query.filter_by(user_id=user_id).all()

    if not reports:
        return [], 200  

    return [report.to_dict() for report in reports], 200


