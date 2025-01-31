from flask import Blueprint, request, abort, make_response
from ..models.stock_movement import StockMovement
from ..models.products import Products
from ..db import db
from datetime import datetime
from app.routes.route_utilities import validate_model

bp = Blueprint("stock_movement_bp", __name__, url_prefix="/stock_movement")

@bp.post("")
def create_stock_movement():
  request_body = request.get_json()

  try:
    product = Products.query.get_or_404(request_body.get("product_id"))
    request_body["sku"] = product.sku

    new_stock_movement = StockMovement.from_dict(request_body)
  except KeyError as e:
    missing_key = e.args[0]
    response = {"details": f"Invalid request body: Missing key '{missing_key}'"}
    abort(make_response(response, 400))

  db.session.add(new_stock_movement)
  db.session.commit()

  response = {"stock_movement": new_stock_movement.to_dict()}
  return response, 201

@bp.get("")
def get_stock_movements():
  try:
    stock_movements = StockMovement.query.all()
    stock_movements_response = [sm.to_dict() for sm in stock_movements]
    return stock_movements_response, 200
  except Exception as e:
    return {"error": "An error occured while fetching stock movements."}, 500
  
@bp.get("/<stock_movement_id>")
def get_one_stock_movement(stock_movement_id):
  stock_movement = validate_model(StockMovement, stock_movement_id)
  if not stock_movement:
    abort(make_response({"message": f"stock_movement_id {stock_movement_id} not found"}, 404))
  
  response = {"stock_movement": stock_movement.to_dict()}
  return response, 200

@bp.put("/<stock_movement_id>")
def update_stock_movement(stock_movement_id):
  stock_movement = validate_model(StockMovement, stock_movement_id)
  request_body = request.get_json()

  try:
    product = Products.query.get_or_404(request_body.get("product_id"))
    request_body["sku"] = product.sku

    for key, value in request_body.items():
      if key != "id":
        setattr(stock_movement, key, value)

    db.session.commit()
  except KeyError as e:
        missing_key = e.args[0]
        response = {"details": f"Invalid request body: Missing key '{missing_key}'"}
        abort(make_response(response, 400))

  return {"message": f"Stock movement {stock_movement_id} successfully updated",
          "stock_movement": stock_movement.to_dict()}, 200

@bp.delete("/<stock_movement_id>")
def delete_stock_movement(stock_movement_id):
  stock_movement = validate_model(StockMovement, stock_movement_id)

  db.session.delete(stock_movement)
  db.session.commit()

  return {"message": f"Stock movement {stock_movement_id} successfully deleted"}, 200