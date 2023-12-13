from flask import Flask, render_template, request, redirect, url_for, session
from models import (
    db,
    Student,
    Professor,
    Assistant,
    Course,
    Admin,
    student_course,
    get_student_by_id,
)

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
            flash(f"Login successful for {{student.frist_name}}.", "success")
            return redirect(url_for("courses_for_student"))
        elif professor:
            flash("Login successful for professor.", "success")
            return redirect("/professor_dashboard")

        elif assistant:
            flash("Login successful for assistant.", "success")
            return redirect("/assistant_dashboard")

        elif admin:
            flash("Login successful for admin.", "success")
            return redirect("/dashboard")

        else:
            flash("Invalid email or password", "danger")
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
        flash('''Signup successful for student
        You will wait your verfication''', "success")
        return redirect(url_for("home"))
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
        flash('''Signup successful for assisstant
        You will wait your verfication''', "success")
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
        flash('''Signup successful for prof
        You will wait your verfication''', "success")
        return redirect(url_for("home"))
    return render_template("sign_up_for_prof.html")


@app.route("/dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if request.method == "POST":
        # Handle enrollment creation when the form is submitted
        user_id = request.form["user_id"]
        user_type = request.form["user_type"]
        course_id = request.form["course_id"]

        if user_type == "student":
            user = Student.query.get(user_id)
        elif user_type == "professor":
            user = Professor.query.get(user_id)
        elif user_type == "assistant":
            user = Assistant.query.get(user_id)
        else:
            return "Invalid user type"

        if user is not None:
            course = Course.query.get(course_id)
            # Add the course to the user's courses relationship
            user.courses.append(course)
            db.session.commit()
        else:
            return "User not found"

    # Retrieve data for displaying on the admin dashboard
    students = Student.query.all()
    professors = Professor.query.all()
    assistants = Assistant.query.all()
    courses = Course.query.all()

    return render_template(
        "dashboard.html",
        students=students,
        professors=professors,
        assistants=assistants,
        courses=courses,
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
    # Your view logic here
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
        professor = get_professor_by_id(professor_id)
    return render_template("professor_dashboard.html")


@app.route("/assistant_dashboard")
def assistant_dashboard():
    assistant_id = session.get("user_id")
    if assistant_id is not None:
        assistant = get_ass_by_id(student_id)
    return render_template("ass_professor_dashboard.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
