from flask import Blueprint, request, abort, make_response
from ..models.reports import Reports
from ..db import db
from ..models.products import Products
from app.routes.route_utilities import validate_model

bp = Blueprint("report_bp", __name__, url_prefix="/reports")

@bp.post("")
def create_reports():
    data = request.get_json()
    product_id = data.get("product_id")
    user_id = data.get("user_id")
    quantity_sold = data.get("quantity_sold", 0)
    stock_movement = data.get("stock_movement", 0)
    
    product = validate_model(Products, product_id)
    if not product:
        abort(make_response({"message": f"product_id {product_id} not found"}, 404))

    if not user_id:
        abort(make_response({"message": "user_id is required"}, 400))
    
    new_report = Reports(
        product_id=product_id,
        use_id=user_id,
        quantity_sold=quantity_sold,
        stock_movement=stock_movement
    )
    db.session.add(new_report)
    db.session.commit()

    response = {"report": new_report.to_dict()}

    return response, 200

@bp.get("")
def get_all_reports():
    try:
        user_id = request.args.get("user_id")

        if not user_id:
            return {"error": "User ID is required to fetch reports"}, 400

        reports = Reports.query.filter_by(user_id=user_id).all()

        if not reports:
            return {"error": "No reports found for this user"}, 404

        return [report.to_dict() for report in reports], 200
    except Exception as e:
        print(f"Error fetching reports: {e}")  
        return {"error": "An error occurred while fetching reports."}, 500

