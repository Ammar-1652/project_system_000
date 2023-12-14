from models import  *
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
db = SQLAlchemy()




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Update with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Change this to a secure secret key
db = SQLAlchemy(app)

# Define the association tables
student_course = db.Table(
    "student_course",
    db.Column("student_id", db.Integer, db.ForeignKey("student.id"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id"), primary_key=True),
)

student_assignment = db.Table(
    "student_assignment",
    db.Column("student_id", db.Integer, db.ForeignKey("student.id"), primary_key=True),
    db.Column("assignment_id", db.Integer, db.ForeignKey("assignment.id"), primary_key=True),
    extend_existing=True  # Add this parameter
)

# Define the models
class StudentAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"))

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    file_url = db.Column(db.String(255))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    dead_line_date = db.Column(db.DateTime)

    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    professor_id = db.Column(db.Integer, db.ForeignKey("professor.id"))
    students = db.relationship("Student", secondary=student_assignment, back_populates="assignments")

# ... (other parts of the code)




class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    contact_number = db.Column(db.String(15), unique=True)
    national_id = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(100), unique=True)
    date_of_birth = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    class_level = db.Column(db.String(10))
    password = db.Column(db.String(100))
    is_verified = db.Column(db.Boolean, default=False)

    assignments = db.relationship("Assignment", secondary=student_assignment, back_populates="students")
    courses = db.relationship("Course", secondary=student_course, backref="students")

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    contact_number = db.Column(db.String(15), unique=True)
    national_id = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(100), unique=True)
    date_of_birth = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    password = db.Column(db.String(100))
    is_verified = db.Column(db.Boolean, default=False)

    assignments = db.relationship("Assignment", backref="professor")
    courses = db.relationship("Course", backref="professor")

class Assistant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    contact_number = db.Column(db.String(15), unique=True)
    national_id = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(100), unique=True)
    date_of_birth = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    password = db.Column(db.String(100))
    is_verified = db.Column(db.Boolean, default=False)

    assignments = db.relationship("Assignment", backref="assistant")
    labs = db.relationship("Course", backref="assistant")

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    hours = db.Column(db.Integer)

    professor_id = db.Column(db.Integer, db.ForeignKey("professor.id"))
    assistant_id = db.Column(db.Integer, db.ForeignKey("assistant.id"))
    assignments = db.relationship("Assignment", backref="course")

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    is_verified = db.Column(db.Boolean, default=True)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
