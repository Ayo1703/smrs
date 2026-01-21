# Student Result Management System (SRMS)
# Console-based Python Application using SQLite

import sqlite3

# ===============================
# DATABASE INITIALIZATION
# ===============================

def initialize_database():
    conn = sqlite3.connect("srms.db")
    cursor = conn.cursor()

    # Create students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            matric_no TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)

    # Create results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matric_no TEXT,
            course_code TEXT,
            score INTEGER,
            grade TEXT,
            FOREIGN KEY (matric_no) REFERENCES students(matric_no)
        )
    """)

    conn.commit()
    conn.close()


# ===============================
# GRADE CALCULATION
# ===============================

def calculate_grade(score):
    if score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 45:
        return "D"
    elif score >= 40:
        return "E"
    else:
        return "F"


# ===============================
# FUNCTIONAL REQUIREMENTS
# ===============================

def add_student():
    matric_no = input("Enter Matric Number: ")
    name = input("Enter Student Name: ")
    department = input("Enter Department: ")

    conn = sqlite3.connect("srms.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO students (matric_no, name, department) VALUES (?, ?, ?)",
            (matric_no, name, department)
        )
        conn.commit()
        print("Student registered successfully.")
    except sqlite3.IntegrityError:
        print("Error: Student with this matric number already exists.")

    conn.close()


def add_result():
    matric_no = input("Enter Matric Number: ")
    course_code = input("Enter Course Code: ")
    score = int(input("Enter Score: "))

    grade = calculate_grade(score)

    conn = sqlite3.connect("srms.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE matric_no = ?", (matric_no,))
    student = cursor.fetchone()

    if student:
        cursor.execute(
            "INSERT INTO results (matric_no, course_code, score, grade) VALUES (?, ?, ?, ?)",
            (matric_no, course_code, score, grade)
        )
        conn.commit()
        print("Result added successfully.")
    else:
        print("Error: Student not found.")

    conn.close()


def view_student_result():
    matric_no = input("Enter Matric Number: ")

    conn = sqlite3.connect("srms.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, department FROM students WHERE matric_no = ?", (matric_no,))
    student = cursor.fetchone()

    if not student:
        print("Student not found.")
        conn.close()
        return

    print("\nStudent Name:", student[0])
    print("Department:", student[1])
    print("\nResults:")

    cursor.execute(
        "SELECT course_code, score, grade FROM results WHERE matric_no = ?",
        (matric_no,)
    )
    results = cursor.fetchall()

    if results:
        for result in results:
            print(f"Course Code: {result[0]} | Score: {result[1]} | Grade: {result[2]}")
    else:
        print("No results found.")

    conn.close()


# ===============================
# MAIN MENU (SYSTEM INTERFACE)
# ===============================

def main_menu():
    while True:
        print("\n===== STUDENT RESULT MANAGEMENT SYSTEM (SRMS) =====")
        print("1. Add Student")
        print("2. Add Result")
        print("3. View Student Result")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_result()
        elif choice == "3":
            view_student_result()
        elif choice == "4":
            print("Exiting SRMS...")
            break
        else:
            print("Invalid option. Try again.")


# ===============================
# PROGRAM ENTRY POINT
# ===============================

initialize_database()
main_menu()
