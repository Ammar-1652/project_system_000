# logic.py

# A dictionary to store the lectures and their teachers
lectures = {"biology": "John", "geology": "John", "math": "Mark", "physics": "Mark"}

# A dictionary to store the students and their courses
students = {"Alien": ["physics", "biology", "geology"], "Bob": ["physics", "math"]}

# A dictionary to store the attendance records for each lecture
attendance = {}

# A function to open the attendance for a lecture
def open_attendance(lecture):
    # Check if the lecture is valid
    if lecture not in lectures:
        print("Invalid lecture name.")
        return

    # Check if the attendance is already open
    if lecture in attendance:
        print("Attendance is already open for this lecture.")
        return

    # Create a new entry in the attendance dictionary
    attendance[lecture] = []
    print("Attendance is now open for", lecture)

# A function to close the attendance for a lecture
def close_attendance(lecture):
    # Check if the lecture is valid
    if lecture not in lectures:
        print("Invalid lecture name.")
        return

    # Check if the attendance is open
    if lecture not in attendance:
        print("Attendance is not open for this lecture.")
        return

    # Remove the entry from the attendance dictionary
    record = attendance.pop(lecture)
    print("Attendance is now closed for", lecture)
    print("The following students attended the lecture:", ", ".join(record))

# A function to sign the attendance for a lecture
def sign_attendance(student, lecture):
    # Check if the student is valid
    if student not in students:
        print("Invalid student name.")
        return

    # Check if the lecture is valid
    if lecture not in lectures:
        print("Invalid lecture name.")
        return

    # Check if the student is enrolled in the lecture
    if lecture not in students[student]:
        print("You are not enrolled in this lecture.")
        return

    # Check if the attendance is open
    if lecture not in attendance:
        print("Attendance is not open for this lecture.")
        return

    # Check if the student has already signed the attendance
    if student in attendance[lecture]:
        print("You have already signed the attendance for this lecture.")
        return

    # Add the student to the attendance list
    attendance[lecture].append(student)
    print("You have successfully signed the attendance for", lecture)

# A function to view the attendance records for a teacher
def view_teacher_records(teacher):
    # Check if the teacher is valid
    if teacher not in lectures.values():
        print("Invalid teacher name.")
        return

    # Print the attendance records for each lecture taught by the teacher
    print("Attendance records for", teacher)
    for lecture, record in attendance.items():
        if lectures[lecture] == teacher:
            print(lecture, ":", ", ".join(record))

# A function to view the attendance records for a student
def view_student_records(student):
    # Check if the student is valid
    if student not in students:
        print("Invalid student name.")
        return

    # Print the attendance records for each lecture enrolled by the student
    print("Attendance records for", student)
    for lecture, record in attendance.items():
        if student in record:
            print(lecture, ": Present")
        elif lecture in students[student]:
            print(lecture, ": Absent")
