from flask import Blueprint
from .controllers.product_controller import get_products, add_product, update_product, delete_product
from .controllers.category_controller import get_categories, add_category, update_category, delete_category
from .controllers.customer_controller import get_customers, add_customer, update_customer, delete_customer
from .controllers.order_controller import create_order

ecommerce_bp = Blueprint('ecommerce', __name__)

# Product routes
ecommerce_bp.route('/products', methods=['GET'])(get_products)
ecommerce_bp.route('/products', methods=['POST'])(add_product)
ecommerce_bp.route('/products/<int:product_id>', methods=['PUT'])(update_product)
ecommerce_bp.route('/products/<int:product_id>', methods=['DELETE'])(delete_product)

# Category routes
ecommerce_bp.route('/categories', methods=['GET'])(get_categories)
ecommerce_bp.route('/categories', methods=['POST'])(add_category)
ecommerce_bp.route('/categories/<int:category_id>', methods=['PUT'])(update_category)
ecommerce_bp.route('/categories/<int:category_id>', methods=['DELETE'])(delete_category)

# Customer routes
ecommerce_bp.route('/customers', methods=['GET'])(get_customers)
ecommerce_bp.route('/customers', methods=['POST'])(add_customer)
ecommerce_bp.route('/customers/<int:customer_id>', methods=['PUT'])(update_customer)
ecommerce_bp.route('/customers/<int:customer_id>', methods=['DELETE'])(delete_customer)

# Order routes
ecommerce_bp.route('/orders', methods=['POST'])(create_order)