from flask import Blueprint, request, abort, make_response, Response
from ..db import db, socketio
from app.models.products import Products
from .route_utilities import validate_model
from flask_socketio import emit

bp = Blueprint("products_bp", __name__, url_prefix="/products")

@bp.post("")
def create_products():
    request_body = request.get_json()

    try:
        new_product = Products.from_dict(request_body)
    except KeyError as e:
        missing_key = e.args[0]
        response = {"details": f"Invalid request body: Missing key '{missing_key}'"}
        abort(make_response(response, 400))

    db.session.add(new_product)
    db.session.commit()

    socketio.emit('new-product', {
        'name': new_product.name,
        'sku': new_product.sku
    })

    response = {"product": new_product.to_dict()}
    return response, 201

@bp.get("")
def get_all_products():
    try:
        query = db.select(Products).order_by(Products.id)
        products = db.session.scalars(query).all()

        products_response = [product.to_dict() for product in products]
        return products_response, 200
    except Exception as e:
        print(f"Error fetching products: {e}")  
        return {"error": "An error occurred while fetching products."}, 500
    
@bp.get("/<product_id>")
def get_one_product(product_id):
    product = validate_model(Products, product_id)
    if not product:
        abort(make_response({"message": f"product_id {product_id} not found"}, 404))

    response = {"product": product.to_dict()}
    return response, 200

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

    if product.quantity <= product.reorder_level:
        socketio.emit(
            "low_stock_alert",
            {
                "product_id": product_id,
                "product_name": product.name,
                "quantity": product.quantity,
                "reorder_level": product.reorder_level,
            },
            broadcast=True
        )

    return {"message": f"Product {product_id} successfully updated",
            "product": product.to_dict(),
            }, 200

@bp.delete("/<product_id>")
def delete_product(product_id):
    product = validate_model(Products, product_id)

    db.session.delete(product)
    db.session.commit()

    socketio.emit('delete-product', {
        'name': product.name,
        'sku': product.sku
    })

    return {"message": f"Product {product_id} successfully deleted"}, 200

