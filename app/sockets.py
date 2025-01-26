from flask_socketio import emit
from app import socketio

@socketio.on('connect')
def handle_connect():
    print("A client connected")
    emit('server-message', 'Welcome to the Flask-SocketIO server!')


# Real time notifications: Notify clients about product changes
@socketio.on('product-updated')
def handle_product_update(data):
    print(f"Product updated received: {data}")
    emit('product-update-notification', {
        'message': f"Product {data['name']} has been updated!"
    }, broadcast=True)

# Real time notifications: Notify clients about new products
@socketio.on('new-product')
def handle_new_product(data):
    print(f"New product added: {data}")
    emit('new-product-notification', {
        'message': f"New product {data['name']} has been added."
    }, broadcast=True)

# Real time notifications: Notify clients when a product is deleted
@socketio.on('delete-product')
def handle_delete_product(data):
    print(f"Product deleted: {data}")
    emit('product-delete-notification', {
        'message': f"Product {data['name']} has been  deleted."
    }, broadcast=True)

def emit_notification(user_id, product_name, notification_type):
    message = f"Notification: {notification_type} for product {product_name}."
    emit(
        "new-notification",
        {
            "user_id": user_id,
            "message": message,
        },
        broadcast=True,
        namespace="/",
    )