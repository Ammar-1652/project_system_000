# def add_course(name_,hours_,is_with_lab_):
#     course=Course(name=name_,hours=hours_,is_with_lab=is_with_lab_)
#     with app.app_context():
#         db.session.add(course)
#         db.session.commit()
from app import *
from datetime import datetime


def set_course_day(id_, day: str):
    with app.app_context():
        course = Course.query.filter_by(id=id_).first()
        course.day = day
        with app.app_context():
            app.session.add(course)
            app.session.commit()


def set_course_hour(id_, hour):
    with app.app_context():
        course = Course.query.filter_by(id=id_).first()
        course.hour = hour
        with app.app_context():
            app.session.add(course)
            app.session.commit()


def get_day(id_):
    with app.app_context():
        course = Course.query.filter_by(id=id_).first()
    day_name = course.day.lower()
    if day_name == "saturday":
        day_of_week = 1
    elif day_name == "sunday":
        day_of_week = 2
    elif day_name == "monday":
        day_of_week = 3
    elif day_name == "tuesday":
        day_of_week = 4
    elif day_name == "wednesday":
        day_of_week = 5
    elif day_name == "thursday":
        day_of_week = 6
    return day_of_week


def get_hour(id_):
    with app.app_context():
        course = Course.query.filter_by(id=id_).first()
    return course.hour


def place_setter(id_):
    with app.app_context():
        course = Course.query.filter_by(id=id_).first()

    if course.day == 1 and course.hour == 9:
        course.place = 1
    elif course.day == 1 and course.hour == 11:
        course.place = 2
    elif course.day == 1 and course.hour == 1:
        course.place = 3
    elif course.day == 1 and course.hour == 3:
        course.place = 4
    elif course.day == 1 and course.hour == 5:
        course.place = 5
    elif course.day == 2 and course.hour == 9:
        course.place = 6
    elif course.day == 2 and course.hour == 11:
        course.place = 7
    elif course.day == 2 and course.hour == 1:
        course.place = 8
    elif course.day == 2 and course.hour == 3:
        course.place = 9
    elif course.day == 2 and course.hour == 5:
        course.place = 10
    elif course.day == 3 and course.hour == 9:
        course.place = 11
    elif course.day == 3 and course.hour == 11:
        course.place = 12
    elif course.day == 3 and course.hour == 1:
        course.place = 13
    elif course.day == 3 and course.hour == 3:
        course.place = 14
    elif course.day == 3 and course.hour == 5:
        course.place = 15
    elif course.day == 4 and course.hour == 9:
        course.place = 16
    elif course.day == 4 and course.hour == 11:
        course.place = 17
    elif course.day == 4 and course.hour == 1:
        course.place = 18
    elif course.day == 4 and course.hour == 3:
        course.place = 19
    elif course.day == 4 and course.hour == 5:
        course.place = 20
    elif course.day == 5 and course.hour == 9:
        course.place = 21
    elif course.day == 5 and course.hour == 11:
        course.place = 22
    elif course.day == 5 and course.hour == 1:
        course.place = 23
    elif course.day == 5 and course.hour == 3:
        course.place = 24
    elif course.day == 5 and course.hour == 5:
        course.place = 25
    elif course.day == 6 and course.hour == 9:
        course.place = 26
    elif course.day == 6 and course.hour == 11:
        course.place = 27
    elif course.day == 6 and course.hour == 1:
        course.place = 28
    elif course.day == 6 and course.hour == 3:
        course.place = 29
    elif course.day == 6 and course.hour == 5:
        course.place = 30
