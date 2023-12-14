from flask import Flask, render_template, request, redirect, url_for,session
from models import *
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from app import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Tables.db"
app.config["SECRET_KEY"] = "your_secret_key"
db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Check if the user exists in the students, professors, assistants, and admin tables
        student = Student.query.filter_by(email=email, password=password).first()
        professor = Professor.query.filter_by(email=email, password=password).first()
        assistant = Assistant.query.filter_by(email=email, password=password).first()
        admin = Admin.query.filter_by(email=email, password=password).first()

        if student:
            session["user_id"] = student.id
            return redirect(url_for("courses_for_student"))
        elif professor:
            return redirect("/professor_dashboard")

        elif assistant:
            return redirect("/assistant_dashboard")

        elif admin:
            return redirect("/admin_dashboard")

        else:
            return "Invalid email or password"

    return render_template("log_in.html")


@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")


@app.route("/sign_up_for_students", methods=["GET", "POST"])
def sign_up_for_students():
    if request.method == "POST":
        s = Student(
            first_name=request.form["first-name"],
            middle_name=request.form["middle-name"],
            last_name=request.form["last-name"],
            contact_number=request.form["contact-number"],
            national_id=request.form["national-id"],
            email=request.form["email"],
            date_of_birth=request.form["date-of-birth"],
            gender=request.form["gender"],
            class_level=request.form["class_level"],
            password=request.form["password"],
        )
        db.session.add(s)
        db.session.commit()
    return render_template("sign_up_for_students.html")


@app.route("/sign_up_for_ass_prof", methods=["GET", "POST"])
def sign_up_for_ass_prof():
    if request.method == "POST":
        a = Assistant(
            first_name=request.form["first-name"],
            middle_name=request.form["middle-name"],
            last_name=request.form["last-name"],
            contact_number=request.form["contact-number"],
            national_id=request.form["national-id"],
            email=request.form["email"],
            date_of_birth=request.form["date-of-birth"],
            gender=request.form["gender"],
            password=request.form["password"],
        )
        db.session.add(a)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("sign_up_for_ass_prof.html")


@app.route("/sign_up_for_prof", methods=["GET", "POST"])
def sign_up_for_prof():
    if request.method == "POST":
        p = Professor(
            first_name=request.form["first-name"],
            middle_name=request.form["middle-name"],
            last_name=request.form["last-name"],
            contact_number=request.form["contact-number"],
            national_id=request.form["national-id"],
            email=request.form["email"],
            date_of_birth=request.form["date-of-birth"],
            gender=request.form["gender"],
            password=request.form["password"],
        )
        db.session.add(p)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("sign_up_for_prof.html")


# ... (previous code)

@app.route("/admin_dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if request.method == "POST":
        # Handle verification or rejection when the form is submitted
        action = request.form.get("action")
        user_id = request.form.get("user_id")

        if action == "verify":
            user = None
            for model in [Student, Professor, Assistant]:
                user = model.query.get(user_id)
                if user:
                    break

            if user:
                user.verified = True
                db.session.commit()
                flash("User verified successfully.", "success")
            else:
                flash("User not found.", "danger")

        elif action == "reject":
            user = None
            for model in [Student, Professor, Assistant]:
                user = model.query.get(user_id)
                if user:
                    break

            if user:
                db.session.delete(user)
                db.session.commit()
                flash("User rejected and deleted.", "success")
            else:
                flash("User not found.", "danger")

    # Retrieve all signups from students, professors, and assistants
    unverified_students = Student.query.filter_by(is_verified=False).all()
    unverified_professors = Professor.query.filter_by(is_verified=False).all()
    unverified_assistants = Assistant.query.filter_by(is_verified=False).all()

    return render_template(
        "admin_dashboard.html",
        unverified_students=unverified_students,
        unverified_professors=unverified_professors,
        unverified_assistants=unverified_assistants,
        student=Student,
        professor=Professor,
        assistant=Assistant,
        admin=Admin
    )


@app.route("/student_dashboard")
def student_dashboard():
    # Add logic to display student-specific data
    return render_template("student_dashboard.html")


@app.route("/courses_for_student")
def courses_for_student():
    student_id = session.get("user_id")
    if student_id is not None:
        student = get_student_by_id(student_id)

    return render_template("courses_for_student.html", student=student)

    # Redirect to login if the user is not logged in
    return redirect(url_for("log_in"))


@app.route("/timetable_for_student")
def timetable_for_student():
    student_id = session.get("user_id")
    if student_id is not None:
        student = get_student_by_id(student_id)
    return render_template("timetable_for_student.html",student=student)


@app.route("/assignment_for_student")
def assignment_for_student():
    student_id = session.get("user_id")
    if student_id is not None:
        student = get_student_by_id(student_id)
    return render_template("assignment_for_student.html",student=student)


@app.route("/attendance_for_student")
def attendance_for_student():
    student_id = session.get("user_id")
    if student_id is not None:
        student = get_student_by_id(student_id)
    return render_template("attendance_for_student.html",student=student)


@app.route("/professor_dashboard")
def professor_dashboard():
    professor_id = session.get("user_id")
    if professor_id is not None:
        professor = get_prof_by_id(professor_id)
    return render_template("prof_dashboard.html",professor=Professor)


@app.route("/assistant_dashboard")
def assistant_dashboard():
    assistant_id = session.get("user_id")
    if assistant_id is not None:
        assistant = get_asst_by_id(assistant_id)
    return render_template("ass_professor_dashboard.html",assistant=assistant)




# ...

@app.route('/professor_assignment', methods=['GET', 'POST'])
def professor_assignment():
    if request.method == 'POST':
        task_description = request.form['task_description']
        deadline_str = request.form['deadline']
        professor_email = request.form['professor_email']
        course_name = request.form['course_name']
        file = request.files['file']

        # Convert the deadline string to a datetime object
        deadline = datetime.strptime(deadline_str, "%Y-%m-%dT%H:%M")

        # Create a unique filename based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{secure_filename(file.filename)}"
        file_path = os.path.join("static", "assignments", filename)

        # Save the file to the static/assignments folder
        file.save(file_path)

        # Save task details to the database
        professor = Professor.query.filter_by(email=professor_email).first()

        # Check if the professor and course exist
        if professor is not None:
            course = Course.query.filter_by(name=course_name.upper()).first()

            # Check if the course exists
            if course is not None:
                task = Assignment(
                    title=task_description,
                    description=task_description,
                    file_url=file_path,
                    dead_line_date=deadline,
                    course_id=course.id,
                    professor_id=professor.id
                )

                db.session.add(task)
                db.session.commit()

                # Update enrollments (assuming the professor is enrolling all students in the course)
                # Dummy data for enrollment, replace with your actual enrollment logic
                student = Student.query.filter_by(email="student@example.com").first()

                if student is not None:
                    enrollment = student_assignment.insert().values(
                        student_id=student.id,
                        assignment_id=task.id
                    )
                    db.session.execute(enrollment)
                    db.session.commit()

                    flash("Assignment added successfully.", "success")
                    return redirect(url_for('professor_assignment'))

                else:
                    flash("Student not found.", "danger")
            else:
                flash("Course not found.", "danger")
        else:
            flash("Professor not found.", "danger")

    return render_template('professor_assignment.html')


# Student assignment route
@app.route("/assignment_for_student", methods=['GET', 'POST'], endpoint='assignment_for_student_view')
def assignment_for_student():
    student_id = session.get("user_id")
    student = None  # Default value if student_id is None

    if student_id is not None:
        student = get_student_by_id(student_id)
    else:
        # Redirect to login if the user is not logged in
        return redirect(url_for("log_in"))

    return render_template("assignment_for_student.html", student=student)




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
