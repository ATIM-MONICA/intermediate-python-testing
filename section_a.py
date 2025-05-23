from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ------------------------
# Database Models
# ------------------------

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    major = db.Column(db.String(50), nullable=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    credits = db.Column(db.Integer, nullable=False)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    grade = db.Column(db.String(2), nullable=True)

# Create tables
with app.app_context():
    db.create_all()

# ------------------------
# Student CRUD Endpoints
# ------------------------

@app.route('/students', methods=['POST'])
def create_student():
    data = request.json
    try:
        student = Student(
            name=data['name'],
            email=data['email'],
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d') if 'date_of_birth' in data else None,
            major=data.get('major')
        )
        db.session.add(student)
        db.session.commit()
        return jsonify({'message': 'Student created', 'id': student.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 409

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([
        {
            'id': s.id,
            'name': s.name,
            'email': s.email,
            'date_of_birth': s.date_of_birth.isoformat() if s.date_of_birth else None,
            'major': s.major
        } for s in students
    ]), 200

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify({
        'id': student.id,
        'name': student.name,
        'email': student.email,
        'date_of_birth': student.date_of_birth.isoformat() if student.date_of_birth else None,
        'major': student.major
    }), 200

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    data = request.json
    student.name = data.get('name', student.name)
    student.email = data.get('email', student.email)
    student.major = data.get('major', student.major)
    if 'date_of_birth' in data:
        student.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
    try:
        db.session.commit()
        return jsonify({'message': 'Student updated'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 409

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    db.session.delete(student)
    db.session.commit()
    return '', 204

# ------------------------
# Course CRUD Endpoints
# ------------------------

@app.route('/courses', methods=['POST'])
def create_course():
    data = request.json
    course = Course(
        title=data['title'],
        description=data.get('description'),
        credits=data['credits']
    )
    db.session.add(course)
    db.session.commit()
    return jsonify({'message': 'Course created', 'id': course.id}), 201

@app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([
        {
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'credits': c.credits
        } for c in courses
    ]), 200

@app.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    return jsonify({
        'id': course.id,
        'title': course.title,
        'description': course.description,
        'credits': course.credits
    }), 200

@app.route('/courses/<int:id>', methods=['PUT'])
def update_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    data = request.json
    course.title = data.get('title', course.title)
    course.description = data.get('description', course.description)
    course.credits = data.get('credits', course.credits)
    db.session.commit()
    return jsonify({'message': 'Course updated'}), 200

@app.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    db.session.delete(course)
    db.session.commit()
    return '', 204

# ------------------------
# Enrollment CRUD Endpoints
# ------------------------

@app.route('/enrollments', methods=['POST'])
def create_enrollment():
    data = request.json
    enrollment = Enrollment(
        student_id=data['student_id'],
        course_id=data['course_id'],
        grade=data.get('grade')
    )
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'message': 'Enrollment created', 'id': enrollment.id}), 201

@app.route('/enrollments', methods=['GET'])
def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify([
        {
            'id': e.id,
            'student_id': e.student_id,
            'course_id': e.course_id,
            'grade': e.grade
        } for e in enrollments
    ]), 200

@app.route('/enrollments/<int:id>', methods=['GET'])
def get_enrollment(id):
    enrollment = Enrollment.query.get(id)
    if not enrollment:
        return jsonify({'error': 'Enrollment not found'}), 404
    return jsonify({
        'id': enrollment.id,
        'student_id': enrollment.student_id,
        'course_id': enrollment.course_id,
        'grade': enrollment.grade
    }), 200

@app.route('/enrollments/<int:id>', methods=['PUT'])
def update_enrollment(id):
    enrollment = Enrollment.query.get(id)
    if not enrollment:
        return jsonify({'error': 'Enrollment not found'}), 404
    data = request.json
    enrollment.student_id = data.get('student_id', enrollment.student_id)
    enrollment.course_id = data.get('course_id', enrollment.course_id)
    enrollment.grade = data.get('grade', enrollment.grade)
    db.session.commit()
    return jsonify({'message': 'Enrollment updated'}), 200

@app.route('/enrollments/<int:id>', methods=['DELETE'])
def delete_enrollment(id):
    enrollment = Enrollment.query.get(id)
    if not enrollment:
        return jsonify({'error': 'Enrollment not found'}), 404
    db.session.delete(enrollment)
    db.session.commit()
    return '', 204

# ------------------------
# Run the App
# ------------------------

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, request, jsonify
from uuid import uuid4

app = Flask(__name__)

# ==================== MODELS ====================

class Product:
    """Product model with name, price, and description"""
    def __init__(self, name, price, description):
        self.id = str(uuid4())
        self.name = name
        self.price = price
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description
        }


class Student:
    """Student model with name, age, and program"""
    def __init__(self, name, age, program):
        self.id = str(uuid4())
        self.name = name
        self.age = age
        self.program = program

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "program": self.program
        }

    def update(self, data):
        self.name = data.get("name", self.name)
        self.age = data.get("age", self.age)
        self.program = data.get("program", self.program)


class Book:
    """Book model with title, author, and year"""
    def __init__(self, title, author, year):
        self.id = str(uuid4())
        self.title = title
        self.author = author
        self.year = year

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year
        }

    def update(self, data):
        self.title = data.get("title", self.title)
        self.author = data.get("author", self.author)
        self.year = data.get("year", self.year)


# ==================== DATA STORAGE ====================
products = {}
students = {}
books = {}

# ==================== PRODUCT CONTROLLERS ====================

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify([product.to_dict() for product in products.values()]), 200

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product(data['name'], data['price'], data['description'])
    products[product.id] = product
    return jsonify(product.to_dict()), 201

@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    if id in products:
        del products[id]
        return jsonify({"message": "Product deleted"}), 200
    return jsonify({"error": "Product not found"}), 404


# ==================== STUDENT CONTROLLERS ====================

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    student = Student(data['name'], data['age'], data['program'])
    students[student.id] = student
    return jsonify(student.to_dict()), 201

@app.route('/students/<id>', methods=['GET'])
def get_student(id):
    student = students.get(id)
    return jsonify(student.to_dict()) if student else (jsonify({"error": "Student not found"}), 404)

@app.route('/students/<id>', methods=['PUT'])
def update_student(id):
    student = students.get(id)
    if student:
        student.update(request.get_json())
        return jsonify(student.to_dict()), 200
    return jsonify({"error": "Student not found"}), 404


# ==================== BOOK CONTROLLERS ====================

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify([book.to_dict() for book in books.values()]), 200

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    book = Book(data['title'], data['author'], data['year'])
    books[book.id] = book
    return jsonify(book.to_dict()), 201

@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    book = books.get(id)
    if book:
        book.update(request.get_json())
        return jsonify(book.to_dict()), 200
    return jsonify({"error": "Book not found"}), 404

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    if id in books:
        del books[id]
        return jsonify({"message": "Book deleted"}), 200
    return jsonify({"error": "Book not found"}), 404


# ==================== PYTHON LOGIC FROM SCREENSHOTS ====================

def get_grade(score):
    """Returns letter grade for a given percentage"""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    elif score >= 50:
        return "E"
    else:
        return "Fail"

def celsius_to_fahrenheit(celsius):
    """Converts Celsius to Fahrenheit"""
    return (9 / 5) * celsius + 32

def area_of_triangle(base, height):
    """Calculates area of a triangle using A = 0.5 * b * h"""
    return 0.5 * base * height


# ==================== DEMO OUTPUT ====================
if __name__ == '__main__':
    print("Grade for 85%:", get_grade(85))  # B
    print("25°C in Fahrenheit:", celsius_to_fahrenheit(25))  # 77.0
    print("Area of triangle (base=2, height=3):", area_of_triangle(2, 3))  # 3.0

    app.run(debug=True)

