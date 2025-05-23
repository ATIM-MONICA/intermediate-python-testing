from app.extensions import db
from datetime import datetime
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'