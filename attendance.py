# app.py
from flask import Flask, render_template, request
from logic import open_attendance, close_attendance, sign_attendance, view_teacher_records, view_student_records

app = Flask(__name__)

# A function to render the homepage
@app.route('/')
def home():
    return render_template('index.html')

# A function to handle teacher actions
@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    if request.method == 'POST':
        teacher_name = request.form['teacher_name']
        action = request.form['action']

        if action == 'open':
            lecture = request.form['lecture']
            open_attendance(lecture)
        elif action == 'close':
            lecture = request.form['lecture']
            close_attendance(lecture)
        elif action == 'view':
            return render_template('teacher_records.html', teacher_name=teacher_name, records=view_teacher_records(teacher_name))

    return render_template('teacher.html')

# A function to handle student actions
@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        student_name = request.form['student_name']
        action = request.form['action']

        if action == 'sign':
            lecture = request.form['lecture']
            sign_attendance(student_name, lecture)
        elif action == 'view':
            return render_template('student_records.html', student_name=student_name, records=view_student_records(student_name))

    return render_template('student.html')

if __name__ == '__main__':
    app.run(debug=True)
