from flask import Blueprint, request, jsonify
from app.models.category import Category
from app.status_codes import *
from app.extensions import db

category_bp = Blueprint('category_bp', __name__, url_prefix='/api/v1/categories')

@category_bp.get('/')
def get_all_categories():
    categories = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories]), HTTP_200_OK

@category_bp.post('/')
def create_category():
    data = request.get_json()
    try:
        new_category = Category(name=data['name'])
        db.session.add(new_category)
        db.session.commit()
        return jsonify({'message': 'Category created successfully.'}), HTTP_201_CREATED
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@category_bp.put('/<int:category_id>')
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), HTTP_404_NOT_FOUND
    data = request.get_json()
    category.name = data.get('name', category.name)
    db.session.commit()
    return jsonify({'message': 'Category updated successfully'}), HTTP_200_OK

@category_bp.delete('/<int:category_id>')
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), HTTP_404_NOT_FOUND
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully'}), HTTP_200_OK