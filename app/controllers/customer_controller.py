from flask import Blueprint, request, jsonify
from app.models.customer import Customer
from app.status_codes import *
from app.extensions import db

customer_bp = Blueprint('customer_bp', __name__, url_prefix='/api/v1/customers')

@customer_bp.get('/')
def get_all_customers():
    customers = Customer.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'email': c.email} for c in customers]), HTTP_200_OK

@customer_bp.post('/')
def create_customer():
    data = request.get_json()
    try:
        new_customer = Customer(name=data['name'], email=data['email'])
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Customer created successfully.'}), HTTP_201_CREATED
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@customer_bp.put('/<int:customer_id>')
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), HTTP_404_NOT_FOUND
    data = request.get_json()
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'}), HTTP_200_OK

@customer_bp.delete('/<int:customer_id>')
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), HTTP_404_NOT_FOUND
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), HTTP_200_OK
