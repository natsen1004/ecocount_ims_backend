from flask import Blueprint, request, abort, make_response
from ..db import db
from app.models.products import Products
from app.models.user import User
from .route_utilities import validate_model
from flask_login import login_required, current_user

bp = Blueprint("products_bp", __name__, url_prefix="/products")

@bp.post("")
@login_required
def create_products():
    request_body = request.get_json()

    try:
        new_product = Products.from_dict(request_body)
        new_product.user_id = current_user.id 
    except KeyError as e:
        missing_key = e.args[0]
        response = {"details": f"Invalid request body: Missing key '{missing_key}'"}
        abort(make_response(response, 400))

    db.session.add(new_product)
    db.session.commit()

    response = {"product": new_product.to_dict()}
    return response, 201

@bp.get("")
@login_required
def get_all_products():
    try:
        if not current_user.is_authenticated:
            print("User is not authenticated.")
            return {"error": "User not authenticated"}, 401

        print("Fetching products for user:", current_user.id)
        
        products = Products.query.filter_by(user_id=current_user.id).all()
        
        if not products:
            print("No products found for this user.")
        products_response = [product.to_dict() for product in products]
        
        print("Products retrieved:", products_response)
        return products_response, 200

    except Exception as e:
        print(f"Error fetching products: {e}")  
        return {"error": "An error occurred while fetching products.", "details": str(e)}, 500

    
@bp.get("/<product_id>")
def get_one_product(product_id):
    product = validate_model(Products, product_id)
    if not product:
        abort(make_response({"message": f"product_id {product_id} not found"}, 404))

    response = {"product": product.to_dict()}
    return response, 200
@bp.get("/<user_id>")
@login_required  
def get_products_by_user_id(user_id):
    try:
        if current_user.id != user_id:
            return {"error": "Unauthorized"}, 403
        
        products = Products.query.filter_by(user_id=user_id).all()

        if not products:
            return {"error": "No products found for this user."}, 404

        products_response = [product.to_dict() for product in products]
        return products_response, 200
    except Exception as e:
        return {"error": f"An error occurred while fetching products: {str(e)}"}, 500


@bp.put("/<product_id>")
def update_product(product_id):
    product = validate_model(Products, product_id)
    request_body = request.get_json()

    product.name = request_body["name"]
    product.sku = request_body["sku"]
    product.quantity = request_body["quantity"]
    product.reorder_level = request_body["reorder_level"]
    product.price = request_body["price"]

    db.session.commit()

    return {
        "message": f"Product {product_id} successfully updated",
        "product": product.to_dict(),
    }, 200

@bp.delete("/<product_id>")
def delete_product(product_id):
    product = validate_model(Products, product_id)

    db.session.delete(product)
    db.session.commit()

    return {"message": f"Product {product_id} successfully deleted"}, 200


