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
