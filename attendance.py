# attendance.py

from flask import Flask, render_template, request
from attendance_logic import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('attendance.html')

@app.route('/professor', methods=['GET', 'POST'])
def professor():
    if request.method == 'POST':
        professor_name = request.form['professor_name']
        action = request.form['action']

        if action == 'open':
            lecture_title = request.form['lecture']
            open_attendance(lecture_title)
        elif action == 'close':
            lecture_title = request.form['lecture']
            close_attendance(lecture_title)
        elif action == 'view':
            return render_template('professor_records.html', professor_name=professor_name, records=view_professor_records(professor_name))

    return render_template('professor.html')

@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        student_name = request.form['student_name']
        action = request.form['action']

        if action == 'sign':
            lecture_title = request.form['lecture']
            sign_attendance(student_name, lecture_title)
        elif action == 'view':
            return render_template('student_records.html', student_name=student_name, records=view_student_records(student_name))

    return render_template('student.html')

if __name__ == '__main__':
    app.run(debug=True)
