from flask import Blueprint, request, abort, make_response
from ..models.reports import Reports
from ..db import db
from ..models.products import Products
from app.routes.route_utilities import validate_model
from flask_jwt_extended import get_jwt_identity, jwt_required

bp = Blueprint("report_bp", __name__, url_prefix="/reports")

@bp.post("")
def create_reports():
    data = request.get_json()
    product_id = data.get("product_id")
    quantity_sold = data.get("quantity_sold", 0)
    stock_movement = data.get("stock_movement", 0)
    
    product = validate_model(Products, product_id)
    if not product:
        abort(make_response({"message": f"product_id {product_id} not found"}, 404))
    
    new_report = Reports(
        product_id=product_id,
        quantity_sold=quantity_sold,
        stock_movement=stock_movement
    )
    db.session.add(new_report)
    db.session.commit()

    response = {"report": new_report.to_dict()}

    return response, 200

@bp.get("")
@jwt_required()
def get_all_reports():
    user_id = get_jwt_identity()

    try:
        query = db.select(Reports).where(Reports.user_id == user_id).order_by(Reports.id)
        reports = db.session.scalars(query).all()

        reports_response = [report.to_dict() for report in reports]
        return reports_response, 200
    except Exception as e:
        print(f"Error fetching reports: {e}")  
        return {"error": "An error occurred while fetching reports."}, 500