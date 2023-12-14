def add_course(name_,hours_,is_with_lab_):
    course=Course(name=name_,hours=hours_,is_with_lab=is_with_lab_)
    with app.app_context():
        db.session.add(course)
        db.session.commit()