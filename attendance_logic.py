# attendance_logic.py

from models import Lecture, Student, Professor
from flask import current_app, flash

def open_attendance(lecture_title):
    with current_app.app_context():
        lecture = Lecture.query.filter_by(title=lecture_title).first()
        if lecture:
            # Check if attendance is already open
            if not lecture.attendance_open:
                lecture.attendance_open = True
                lecture.save()
                flash(f"Attendance is now open for {lecture_title}", 'success')
            else:
                flash(f"Attendance is already open for {lecture_title}", 'info')
        else:
            flash("Invalid lecture title.", 'danger')

def close_attendance(lecture_title):
    with current_app.app_context():
        lecture = Lecture.query.filter_by(title=lecture_title).first()
        if lecture:
            # Check if attendance is open
            if lecture.attendance_open:
                lecture.attendance_open = False
                lecture.save()
                flash(f"Attendance is now closed for {lecture_title}", 'success')
            else:
                flash(f"Attendance is not open for {lecture_title}", 'info')
        else:
            flash("Invalid lecture title.", 'danger')

def sign_attendance(student_name, lecture_title):
    with current_app.app_context():
        student = Student.query.filter_by(first_name=student_name).first()
        lecture = Lecture.query.filter_by(title=lecture_title).first()

        if student and lecture:
            # Check if the student is enrolled in the lecture
            if lecture in student.lectures_attendance:
                # Check if attendance is open
                if lecture.attendance_open:
                    # Check if the student has already signed the attendance
                    if student not in lecture.students_attendance:
                        lecture.students_attendance.append(student)
                        lecture.save()
                        flash(f"You have successfully signed the attendance for {lecture_title}", 'success')
                    else:
                        flash(f"You have already signed the attendance for {lecture_title}", 'info')
                else:
                    flash(f"Attendance is not open for {lecture_title}", 'info')
            else:
                flash(f"You are not enrolled in {lecture_title}", 'danger')
        else:
            flash("Invalid student or lecture.", 'danger')

def view_professor_records(professor_name):
    with current_app.app_context():
        lectures_taught = Lecture.query.filter_by(professor_id=professor_name).all()
        records = []

        for lecture in lectures_taught:
            records.append({
                'lecture_title': lecture.title,
                'students_attendance': [student.first_name for student in lecture.students_attendance]
            })

        return records

def view_student_records(student_name):
    with current_app.app_context():
        student = Student.query.filter_by(first_name=student_name).first()

        if student:
            records = []

            for lecture in student.lectures_attendance:
                if student in lecture.students_attendance:
                    records.append({'lecture_title': lecture.title, 'status': 'Present'})
                else:
                    records.append({'lecture_title': lecture.title, 'status': 'Absent'})

            return records
        else:
            flash("Invalid student name.", 'danger')
