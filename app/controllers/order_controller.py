from flask import Blueprint, request, jsonify
from app.models.order import Order
from app.models.order_item import OrderItem
from app.status_codes import *
from app.extensions import db

order_bp = Blueprint('order_bp', __name__, url_prefix='/api/v1/orders')

@order_bp.post('/')
def create_order():
    data = request.get_json()
    try:
        customer_id = data['customer_id']
        items = data['items']  # List of dicts with product_id and quantity

        new_order = Order(customer_id=customer_id)
        db.session.add(new_order)
        db.session.flush()

        for item in items:
            order_item = OrderItem(order_id=new_order.id, product_id=item['product_id'], quantity=item['quantity'])
            db.session.add(order_item)

        db.session.commit()
        return jsonify({'message': 'Order created successfully', 'order_id': new_order.id}), HTTP_201_CREATED
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

