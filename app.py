from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from models import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Tables.db"
app.config["SECRET_KEY"] = "your_secret_key"
db.init_app(app)

accounts = []


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
        admin = Admin.query.filter_by(email="admin@gmail.com", password="admin").first()

        if student:
            session["user_id"] = student.id 
            if student.is_verified==True:
                flash("Login successful" ,  "success")
                return redirect(url_for("courses_for_student"))
        elif professor:
            session["user_id"] = professor.id
            if professor.is_verified==True:
                flash("Login successful" ,  "success")
                return redirect(url_for("courses_for_professor"))
            

        elif assistant:
            session["user_id"] = assistant.id
            if assistant.is_verified==True:
                flash("Login successful" ,  "success")
                return redirect(url_for("courses_for_assistant"))
            

        elif admin:
            flash("Login successful" ,  "success")
            return redirect("/verification_for_admin")

        else:
            flash("Login faild" ,  "danger")
            return "Invalid email or password"

    return render_template("log_in.html")


@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@app.route("/sign_up_for_students", methods=["GET", "POST"])
def sign_up_for_students():
    if request.method == "POST":
        account = Student(
            first_name=request.form.get("first-name"),
            middle_name=request.form.get("middle-name"),
            last_name=request.form.get("last-name"),
            contact_number=request.form.get("contact-number"),
            national_id=request.form.get("national-id"),
            email=request.form.get("email"),
            date_of_birth=request.form.get("date-of-birth"),
            gender=request.form.get("gender"),
            class_level=request.form.get("class_level"),
            password=request.form.get("password"),
        )

        db.session.add(account)
        db.session.commit()

        flash("Sign_up successful\n Wait for verification", "success")
        return redirect("log_in")  # Replace "your_redirect_route" with the appropriate route after successful signup.

    return render_template("sign_up_for_students.html")


@app.route("/sign_up_for_ass_prof", methods=["GET", "POST"])
def sign_up_for_ass_prof():
    if request.method == "POST":
        account = Assistant(
            first_name=request.form.get("first-name"),
            middle_name=request.form.get("middle-name"),
            last_name=request.form.get("last-name"),
            contact_number=request.form.get("contact-number"),
            national_id=request.form.get("national-id"),
            email=request.form.get("email"),
            date_of_birth=request.form.get("date-of-birth"),
            gender=request.form.get("gender"),
            password=request.form.get("password"),
        )

        db.session.add(account)
        db.session.commit()
        accounts.append(account)
        flash("Sign_up successful\n Wait for verification", "success")
        return redirect("log_in")
    return render_template("sign_up_for_ass_prof.html")


@app.route("/sign_up_for_prof", methods=["GET", "POST"])
def sign_up_for_prof():
    if request.method == "POST":
        account = Professor(
            first_name=request.form.get("first-name"),
            middle_name=request.form.get("middle-name"),
            last_name=request.form.get("last-name"),
            contact_number=request.form.get("contact-number"),
            national_id=request.form.get("national-id"),
            email=request.form.get("email"),
            date_of_birth=request.form.get("date-of-birth"),
            gender=request.form.get("gender"),
            password=request.form.get("password"),
        )

        db.session.add(account)
        db.session.commit()
        flash("Sign_up successful\n Wait for verification", "success")
        return redirect("log_in")
    return render_template("sign_up_for_prof.html")




@app.route("/admin_dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if request.method == "POST":
        render_template("admin_dashboard.html")


@app.route("/student_dashboard")
def student_dashboard():
    # Add logic to display student-specific data
    return render_template("student_dashboard.html", accounts=accounts)




@app.route("/courses_for_student")
def courses_for_student():
    student_id = session.get("user_id")
    if student_id is not None:
        student = get_student_by_id(student_id)

    return render_template(
        "courses_for_student.html", student=Student, admin=Admin, courses=Course
    )

    # Redirect to login if the user is not logged in
    return redirect(url_for("log_in"))


@app.route("/timetable_for_student")
def timetable_for_student():
    student_id = session.get("user_id")
    if student_id is not None:
        student = get_student_by_id(student_id)
    return render_template("timetable_for_student.html", student=student)


@app.route("/assignment_for_student")
def assignment_for_student():
    student_id = session.get("user_id")
    if student_id is not None:
        student = get_student_by_id(student_id)
    return render_template("assignment_for_student.html", student=Student)


@app.route("/attendance_for_student")
def attendance_for_student():
    student_id = session.get("user_id")
    if student_id is not None:
        student = get_student_by_id(student_id)
    return render_template("attendance_for_student.html", student=Student)


@app.route("/professor_dashboard")
def professor_dashboard():
    professor_id = session.get("user_id")
    if professor_id is not None:
        professor = get_prof_by_id(professor_id)
    return render_template("prof_dashboard.html", professor=professor)


@app.route("/assistant_dashboard")
def assistant_dashboard():
    assistant_id = session.get("user_id")
    if assistant_id is not None:
        assistant = get_asst_by_id(assistant_id)
    return render_template("ass_professor_dashboard.html", assistant=Assistant)


@app.route("/verification_for_admin", methods=["GET", "POST"])
def verification_for_admin():
    accounts_verification = []
    students = Student.query.all()
    profs = Professor.query.all()
    assts = Assistant.query.all()

    if request.method == "POST":
        account_id = request.form.get("account_id")
        action = request.form.get("action")

        account = None
        # Try to find the account in each table
        account = Student.query.get(account_id) or \
                Professor.query.get(account_id) or \
                Assistant.query.get(account_id)

        if account:
            if action == "verify":
                account.is_verified = True
            elif action == "reject":
                db.session.delete(account)

            db.session.commit()

    for student in students:
        if not student.is_verified:
            accounts_verification.append(student)

    for prof in profs:
        if not prof.is_verified:
            accounts_verification.append(prof)

    for asst in assts:
        if not asst.is_verified:
            accounts_verification.append(asst)

    return render_template(
        "verification_for_admin.html", accounts_verification=accounts_verification
    )

@app.route("/courses_for_admin")
def courses_for_admin():
    if request.method == 'POST':
        name = request.form.get('name')
        hours = request.form.get('hours')
        is_with_lab = request.form.get('is_with_lab')
        course_show = Course.query.all()
        add_course(name, hours,is_with_lab)
        course_show = Course.query.all()
    c=None
    course_show = None
    if request.method == 'POST':
        c = Course(hour=request.form.get('hour'), day=request.form.get('day'))
        db.session.add(c)
        db.session.commit()
    return render_template("courses_for_admin.html", course=c, course_show=course_show)


@app.route("/timetable_for_admin")
def timetable_for_admin():
    # Your view function code here
    return render_template("timetable_for_admin.html")


@app.route("/profs_for_admin")
def profs_for_admin():
    prof_id=request.args.get('prof_id')
    profs=Professor.query.all()
    prof=get_prof_by_id(prof_id)
    return render_template("profs_for_admin.html",profs=profs ,prof=prof)


@app.route("/ass_prof_for_admin")
def ass_prof_for_admin():
    asst_id=request.args.get('asst_id')
    assts=Assistant.query.all()
    asst=get_asst_by_id(asst_id)
    # Add logic to display student-specific data
    return render_template("ass_prof_for_admin.html",asst=asst,assts=assts)


@app.route("/students_for_admin")
def students_for_admin():
    student_id = request.args.get('student_id')
    students = Student.query.all()
    student = get_student_by_id(student_id)
    return render_template("students_for_admin.html", student=student, students=students)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
