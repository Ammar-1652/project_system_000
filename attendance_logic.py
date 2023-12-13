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

# A loop to prompt the user for input
while True:
  # Ask the user if they are a teacher or a student
  user = input("Are you a teacher or a student? (Type 'exit' to quit) ")
  # Exit the program if the user types 'exit'
  if user == "exit":
    break
  # Handle the teacher input
  elif user == "teacher":
    # Ask the teacher for their name
    teacher = input("What is your name? ")
    # Ask the teacher what they want to do
    action = input("Do you want to open, close, or view the attendance? ")
    # Handle the open action
    if action == "open":
      # Ask the teacher for the lecture name
      lecture = input("What is the name of the lecture? ")
      # Call the open_attendance function
      open_attendance(lecture)
    # Handle the close action
    elif action == "close":
      # Ask the teacher for the lecture name
      lecture = input("What is the name of the lecture? ")
      # Call the close_attendance function
      close_attendance(lecture)
    # Handle the view action
    elif action == "view":
      # Call the view_teacher_records function
      view_teacher_records(teacher)
    # Handle the invalid action
    else:
      print("Invalid action.")
  # Handle the student input
  elif user == "student":
    # Ask the student for their name
    student = input("What is your name? ")
    # Ask the student what they want to do
    action = input("Do you want to sign or view the attendance? ")
    # Handle the sign action
    if action == "sign":
      # Ask the student for the lecture name
      lecture = input("What is the name of the lecture? ")
      # Call the sign_attendance function
      sign_attendance(student, lecture)
    # Handle the view action
    elif action == "view":
      # Call the view_student_records function
      view_student_records(student)
    # Handle the invalid action
    else:
      print("Invalid action.")
  # Handle the invalid input
  else:
    print("Invalid input.")
