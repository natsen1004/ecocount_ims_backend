from flask import Blueprint, request, abort, make_response
from ..db import db
from app.models.products import Products
from app.models.user import User
from .route_utilities import validate_model
from app.services.notification_service import send_notification

bp = Blueprint("products_bp", __name__, url_prefix="/products")

@bp.post("")
def create_product():
    request_body = request.get_json()
    user_id = request_body.get("user_id")

    if not user_id or not User.query.get(user_id):
        abort(make_response({"error": "Valid user_id is required"}, 400))

    new_product = Products.from_dict(request_body)
    db.session.add(new_product)
    db.session.commit()

    message = f"New product added: {new_product.name} (SKU: {new_product.sku})"
    send_notification(user_id, message, db.session, "Product Added", new_product.id)

    return {"product": new_product.to_dict()}, 201

@bp.get("")
def get_all_products():
    user_id = request.args.get("user_id")
    if not user_id or not User.query.get(user_id):
        abort(make_response({"error": "Valid user_id is required"}, 400))

    products = Products.query.filter_by(user_id=user_id).all()
    return [product.to_dict() for product in products], 200

@bp.get("/<product_id>")
def get_one_product(product_id):
    product = Products.query.get_or_404(product_id)
    return {"product": product.to_dict()}, 200

@bp.put("/<product_id>")
def update_product(product_id):
    product = Products.query.get_or_404(product_id)
    request_body = request.get_json()

    for key, value in request_body.items():
        if hasattr(product, key):
            setattr(product, key, value)

    db.session.commit()
    return {"message": f"Product {product_id} updated", "product": product.to_dict()}, 200

@bp.delete("/<product_id>")
def delete_product(product_id):
    user_id = request.json.get('user_id')
    if not user_id:
        abort(make_response({"error": "user_id is required"}, 400))

    product = Products.query.filter_by(id=product_id, user_id=user_id).first()
    if not product:
        abort(make_response({"error": "Product not found or unauthorized"}, 404))
    
    product_name = product.name  
    product_sku = product.sku

    db.session.delete(product)
    db.session.commit()

    message = f"Product removed: {product_name} (SKU: {product_sku})"
    send_notification(user_id, message, db.session, "Product Removed", product_id)
    
    return {"message": f"Product {product_id} deleted"}, 200


