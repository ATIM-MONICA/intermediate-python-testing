from flask import Blueprint, request, jsonify
from app.models.product import Product
from app.status_codes import *
from app.extensions import db

product_bp = Blueprint('product_bp', __name__, url_prefix='/api/v1/products')

@product_bp.get('/')
def get_all_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'description': p.description,
        'category_id': p.category_id
    } for p in products]), HTTP_200_OK

@product_bp.post('/')
def create_product():
    data = request.get_json()
    try:
        new_product = Product(
            name=data['name'],
            price=data['price'],
            description=data.get('description'),
            category_id=data['category_id']
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product created successfully.'}), HTTP_201_CREATED
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@product_bp.put('/<int:product_id>')
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), HTTP_404_NOT_FOUND
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.description = data.get('description', product.description)
    product.category_id = data.get('category_id', product.category_id)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'}), HTTP_200_OK

@product_bp.delete('/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), HTTP_404_NOT_FOUND
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), HTTP_200_OK
