#from flask import Flask
#from app.extensions import db,migrate


#application factory function
#def create_app():
    
    #app instance 
    #app = Flask(__name__)
    #app.config.from_object('config.Config')
    
    #db.init_app(app)
    #migrate.init_app(app,db)



    #@app.route("/")
    #def home():
        #return "Python Exam"
    
  
    
    

    #return app

from flask import Flask
from app.extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.product import Product #  Import models for migration detection
    from app.models.category import Category 
    from app.models.customer import Customer
    from app.models.order import Order
    from app.models.order_item import OrderItem 
                 
    #from app.routes import ecommerce_bp        #  Register routes
    #app.register_blueprint(ecommerce_bp)
    
    # Register blueprints for each controller
    from app.controllers.product_controller import product_bp
    from app.controllers.category_controller import category_bp
    from app.controllers.customer_controller import customer_bp
    from app.controllers.order_controller import order_bp

    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(order_bp)

    @app.route("/")
    def home():
        return "Python Exam"

    return app



