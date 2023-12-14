from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from datetime import datetime

db = SQLAlchemy()



student_attendance = db.Table(
    "student_attendance",
    db.Column("student_id", db.Integer, db.ForeignKey("student.id"), primary_key=True),
    db.Column("lecture_id", db.Integer, db.ForeignKey("lecture.id"), primary_key=True),
    db.Column("attended", db.Boolean, default=False),
)

student_course = db.Table("student_course",
    db.Column("student_id", db.Integer, db.ForeignKey("student.id"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id"), primary_key=True)
)

student_assignment=db.Table("student_assignment",
    db.Column("student_id",db.Integer,db.ForeignKey('student.id'),primary_key=True),
    db.Column("assignment_id",db.Integer, db.ForeignKey('assignment.id'),primary_key=True)

)

class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    # professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'))
    # Relationships
    students_attendance = db.relationship('Student', secondary='student_attendance', back_populates='lectures_attendance')
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    file_url = db.Column(db.String(255))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    dead_line_date=db.Column(db.DateTime)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'))
    students = db.relationship('Student', secondary='student_assignment', back_populates='assignments')


def sign_attendance(student_id, lecture_id):
    with current_app.app_context():
        student = get_student_by_id(student_id)
        lecture = get_lecture_by_id(lecture_id)

        if student and lecture:
            student.lectures_attendance.append(lecture)
            db.session.commit()

def view_student_attendance(student_id):
    with current_app.app_context():
        student = get_student_by_id(student_id)

        if student:
            return student.lectures_attendance
        return []

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    contact_number = db.Column(db.String(15),unique=True)
    national_id = db.Column(db.String(20),unique=True)
    email = db.Column(db.String(100), unique=True)
    date_of_birth = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    class_level = db.Column(db.String(10))
    password = db.Column(db.String(100))  
    role=db.Column(db.String,default="student")
    is_verified=db.Column(db.Boolean,default=False)
    
    assignments = db.relationship('Assignment', secondary='student_assignment', back_populates='students')
    
    lectures_attendance = db.relationship('Lecture', secondary='student_attendance', back_populates='students_attendance')

    courses = db.relationship("Course", secondary=student_course, backref="students")

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    contact_number = db.Column(db.String(15),unique=True)
    national_id = db.Column(db.String(20),unique=True)
    email = db.Column(db.String(100), unique=True)
    date_of_birth = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    password = db.Column(db.String(100))
    role=db.Column(db.String,default="professor")

    is_verified=db.Column(db.Boolean,default=False)
    
    assignments = db.relationship('Assignment', backref='professor')

    courses = db.relationship("Course", backref="professor")

class Assistant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    contact_number = db.Column(db.String(15),unique=True)
    national_id = db.Column(db.String(20),unique=True)
    email = db.Column(db.String(100), unique=True)
    date_of_birth = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    password = db.Column(db.String(100))
    role=db.Column(db.String,default="assistant")
    is_verified=db.Column(db.Boolean,default=False)
    

    labs = db.relationship("Course", backref="assistant")

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    hours = db.Column(db.Integer)
    is_with_lab=db.Column(db.Boolean)
    day=db.Column(db.String(50),default=None)
    hour=db.Column(db.Integer,default=None)
    place=db.Column(db.Integer,default=None)
    
    
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'),default=None)
    assistant_id = db.Column(db.Integer, db.ForeignKey('assistant.id'),default=None)
    assignments = db.relationship('Assignment', backref='course')


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    is_verified=db.Column(db.Boolean,default=True)


def get_lecture_by_id(lecture_id):
    with current_app.app_context():
        lecture = Lecture.query.filter_by(id=lecture_id).first()
    return lecture




def get_students():
    with current_app.app_context():
        students=Student.query.all()
    return students

def get_student_by_id(id_):
    with current_app.app_context():
        student=Student.query.filter_by(id=id_).first()
    return student

def get_students_by_first_name(first_name_):
    with current_app.app_context():
        students=Student.query.filter_by(first_name=first_name_).all()
    return students

def get_students_by_middle_name(middle_name_):
    with current_app.app_context():
        students=Student.query.filter_by(middle_name=middle_name_).all()
    return students

def get_students_by_last_name(last_name_):
    with current_app.app_context():
        students=Student.query.filter_by(last_name=last_name_).all()
    return students

def get_student_by_contact_number(contact_number_):
    with current_app.app_context():
        student=Student.query.filter_by(contact_number=contact_number_).first()
    return student

def get_student_by_national_id(national_id_):
    with current_app.app_context():
        student=Student.query.filter_by(national_id_=national_id_).first()
    return student    

def get_student_by_email(email_):
    with current_app.app_context():
        student=Student.query.filter_by(email=email_).first()
    return student

def get_students_by_date_of_birth(date_of_birth_):
    with current_app.app_context():
        student=Student.query.filter_by(date_of_birth=date_of_birth_).first()
    return student
#====================================================================


#==================Professor====================================

def get_profs():
    with current_app.app_context():
        profs=Professor.query.all()
    return profs

def get_prof_by_id(id_):
    with current_app.app_context():
        prof=Professor.query.filter_by(id=id_).first()
    return prof
def get_profs_by_first_name(first_name_):
    with current_app.app_context():
        profs=Professor.query.filter_by(first_name=first_name_).all()
    return profs

def get_profs_by_middle_name(middle_name_):
    with current_app.app_context():
        profs=Professor.query.filter_by(middle_name=middle_name_).all()
    return profs

def get_profs_by_last_name(last_name_):
    with current_app.app_context():
        profs=Professor.query.filter_by(last_name=last_name_).all()
    return profs

def get_prof_by_contact_number(contact_number_):
    with current_app.app_context():
        prof=Professor.query.filter_by(contact_number=contact_number_).first()
    return prof

def get_prof_by_national_id(national_id_):
    with current_app.app_context():
        prof=Professor.query.filter_by(national_id_=national_id_).first()
    return prof    

def get_prof_by_email(email_):
    with current_app.app_context():
        prof=Professor.query.filter_by(email=email_).first()
    return prof

def get_profs_by_date_of_birth(date_of_birth_):
    with current_app.app_context():
        prof=Professor.query.filter_by(date_of_birth=date_of_birth_).first()
    return prof

#====================================================================


#=======================Assistant=====================================

def get_assts():
    with current_app.app_context():
        assts=Assistant.query.all()
    return assts

def get_asst_by_id(id_):
    with current_app.app_context():
        asst=Assistant.query.filter_by(id=id_).first()
    return asst
def get_assts_by_first_name(first_name_):
    with current_app.app_context():
        assts=Assistant.query.filter_by(first_name=first_name_).all()
    return assts

def get_assts_by_middle_name(middle_name_):
    with current_app.app_context():
        assts=Assistant.query.filter_by(middle_name=middle_name_).all()
    return assts

def get_assts_by_last_name(last_name_):
    with current_app.app_context():
        assts=Assistant.query.filter_by(last_name=last_name_).all()
    return assts

def get_asst_by_contact_number(contact_number_):
    with current_app.app_context():
        asst=Assistant.query.filter_by(contact_number=contact_number_).first()
    return asst

def get_asst_by_national_id(national_id_):
    with current_app.app_context():
        asst=Assistant.query.filter_by(national_id_=national_id_).first()
    return asst    

def get_asst_by_email(email_):
    with current_app.app_context():
        asst=Assistant.query.filter_by(email=email_).first()
    return asst

def get_assts_by_date_of_birth(date_of_birth_):
    with current_app.app_context():
        assts=Assistant.query.filter_by(date_of_birth=date_of_birth_).first()
    return assts

#==========================================================================================

#=============================course========================================

def get_course():
    with current_app.app_context():
        courses=Course.query.all()
    return courses

def get_course_by_id(id_):
    with current_app.app_context():
        course=Course.query.filter_by(id=id_).first()
    return course

def get_course_by_name(name_):
    with current_app.app_context():
        course=Course.query.filter_by(name=name_.upper()).first()
        return course

def add_course(name_,hours_,is_with_lab_):
    course=Course(name=name_,hours=hours_,is_with_lab=is_with_lab_)
    with app.app_context():
        db.session.add(course)
        db.session.commit()

