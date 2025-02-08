import json
import os
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# 🔹 Initialize Firebase
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

if firebase_credentials is None:
    st.error("FIREBASE_CREDENTIALS environment variable is not set.")
    st.stop()

firebase_credentials = json.loads(firebase_credentials)

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)

# 🔹 Firestore Client
db = firestore.client()

# 🔹 Helper functions to get references
def get_student_ref(roll_no):
    return db.collection('students').document(roll_no)

def get_attendance_ref(roll_no):
    return db.collection('attendance').document(roll_no)

def get_complaint_ref(roll_no):
    return db.collection('complaints').document(roll_no)

def get_remarks_ref(roll_no):
    return db.collection('remarks').document(roll_no)

# 🔹 Firebase CRUD functions
def add_student(name, roll_no, age, course):
    student_ref = get_student_ref(roll_no)
    student_ref.set({
        'name': name,
        'roll_no': roll_no,
        'age': age,
        'course': course
    })

def delete_student(roll_no):
    student_ref = get_student_ref(roll_no)
    student_ref.delete()

def get_students():
    students_ref = db.collection('students')
    students = students_ref.stream()
    return {student.id: student.to_dict() for student in students}

def add_attendance(roll_no, date, status):
    attendance_ref = get_attendance_ref(roll_no)
    attendance_ref.set({'date': date, 'status': status})

def get_attendance(roll_no):
    attendance_ref = get_attendance_ref(roll_no)
    doc = attendance_ref.get()
    return doc.to_dict() if doc.exists else None

def add_complaint(roll_no, complaint):
    complaint_ref = get_complaint_ref(roll_no)
    complaint_ref.set({'complaint': complaint})

def get_complaint(roll_no):
    complaint_ref = get_complaint_ref(roll_no)
    doc = complaint_ref.get()
    return doc.to_dict() if doc.exists else None

def add_remarks(roll_no, remarks):
    remarks_ref = get_remarks_ref(roll_no)
    remarks_ref.set({'remarks': remarks})

def get_remarks(roll_no):
    remarks_ref = get_remarks_ref(roll_no)
    doc = remarks_ref.get()
    return doc.to_dict() if doc.exists else None

# 🔹 Streamlit UI
st.title('Student Management System')

menu = ['Add Student', 'View Students', 'Delete Student', 'Mark Attendance', 'View Attendance', 'Add Complaint', 'View Complaint', 'Add Remarks', 'View Remarks']
choice = st.sidebar.selectbox('Select an option:', menu)

if choice == 'Add Student':
    st.subheader('Add a new student')
    name = st.text_input('Name')
    roll_no = st.text_input('Roll Number')
    age = st.number_input('Age', min_value=18, max_value=100)
    course = st.text_input('Course')
    
    if st.button('Add Student'):
        add_student(name, roll_no, age, course)
        st.success(f'Student {name} added successfully!')

elif choice == 'View Students':
    st.subheader('View all students')
    students = get_students()
    if students:
        df = pd.DataFrame.from_dict(students, orient='index')
        st.dataframe(df)
    else:
        st.warning('No students found!')

elif choice == 'Delete Student':
    st.subheader('Delete a student')
    roll_no = st.text_input('Roll Number of student to delete')
    if st.button('Delete'):
        delete_student(roll_no)
        st.success(f'Student with Roll Number {roll_no} deleted.')

elif choice == 'Mark Attendance':
    st.subheader('Mark Attendance')
    roll_no = st.text_input('Student Roll Number')
    date = st.date_input('Date')
    status = st.selectbox('Status', ['Present', 'Absent'])
    
    if st.button('Mark Attendance'):
        add_attendance(roll_no, str(date), status)
        st.success(f'Attendance for {roll_no} marked as {status}.')

elif choice == 'View Attendance':
    st.subheader('View Attendance')
    roll_no = st.text_input('Enter Student Roll Number')
    
    if st.button('Fetch Attendance'):
        attendance = get_attendance(roll_no)
        if attendance:
            st.write(f"Date: {attendance['date']}")
            st.write(f"Status: {attendance['status']}")
        else:
            st.warning('No attendance record found.')

elif choice == 'Add Complaint':
    st.subheader('Add Complaint')
    roll_no = st.text_input('Student Roll Number')
    complaint = st.text_area('Complaint')
    
    if st.button('Add Complaint'):
        add_complaint(roll_no, complaint)
        st.success(f'Complaint added for student {roll_no}.')

elif choice == 'View Complaint':
    st.subheader('View Complaint')
    roll_no = st.text_input('Enter Student Roll Number')
    
    if st.button('Fetch Complaint'):
        complaint = get_complaint(roll_no)
        if complaint:
            st.write(f"Complaint: {complaint['complaint']}")
        else:
            st.warning('No complaint record found.')

elif choice == 'Add Remarks':
    st.subheader('Add Remarks')
    roll_no = st.text_input('Student Roll Number')
    remarks = st.text_area('Remarks')
    
    if st.button('Add Remarks'):
        add_remarks(roll_no, remarks)
        st.success(f'Remarks added for student {roll_no}.')

elif choice == 'View Remarks':
    st.subheader('View Remarks')
    roll_no = st.text_input('Enter Student Roll Number')
    
    if st.button('Fetch Remarks'):
        remarks = get_remarks(roll_no)
        if remarks:
            st.write(f"Remarks: {remarks['remarks']}")
        else:
            st.warning('No remarks record found.')
