import sqlite3
import csv
print("Welcome to the Student Management System!")



def get_input(prompt):
    value = input(prompt).strip()

    if value.lower() == "q":
        print("Operation cancelled. Returning to main menu...")
        return None

    return value



def create_database():
    connection = sqlite3.connect("student_management.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL,
            marks INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()
    print("Database ready!")



def add_student():
    print("Add a new student (type q at any prompt to cancel):")

    # Get student name
    while True:
        name = get_input("Enter name: ")

        if name is None:
            return

        name = name.title()

        if name:
            break
        else:
            print("Name cannot be empty.")

    # Get student age
    while True:
        age_input = get_input("Enter age: ")

        if age_input is None:
            return

        try:
            age = int(age_input)

            if 1 <= age <= 100:
                break
            else:
                print("Age must be between 1 and 100.")

        except ValueError:
            print("Please enter a valid number.")

    # Get student course
    while True:
        course = get_input("Enter course: ")

        if course is None:
            return

        course = course.title()

        if course:
            break
        else:
            print("Course cannot be empty.")

    # Get student marks
    while True:
        marks_input = get_input("Enter marks (0-100): ")

        if marks_input is None:
            return

        try:
            marks = int(marks_input)

            if 0 <= marks <= 100:
                break
            else:
                print("Marks must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")

    # Save student to database
    connection = sqlite3.connect("student_management.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students (name, age, course, marks)
        VALUES (?, ?, ?, ?)
    """, (name, age, course, marks))

    connection.commit()
    connection.close()

    print("Student added successfully!")







def view_students():
    connection = sqlite3.connect("student_management.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, age, course, marks
        FROM students
    """)

    students = cursor.fetchall()
    if students:
        print("\n===== Student Records =====")

        for student in students:
            student_id, name, age, course, marks = student
            print(
            f"ID: {student_id} | "
            f"Name: {name} | "
            f"Age: {age} | "
            f"Course: {course} | "
            f"Marks: {marks}"
        )
            
    else:
        print("No student records found.")
            
    
    connection.close()



def search_student():
    while True:
        name = get_input("Enter name to search(or q to cancel): ").strip()
        if name is None:
            return

        if name:
            break
        else:
            print("Name cannot be empty.")

    connection = sqlite3.connect("student_management.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, age, course, marks
        FROM students
        WHERE name LIKE ?
    """, (f"%{name}%",))

    students = cursor.fetchall()

    if students:
        print("\n===== Search Results =====")

        for student in students:
            student_id, name, age, course, marks = student

            print(
                f"ID: {student_id} | "
                f"Name: {name} | "
                f"Age: {age} | "
                f"Course: {course} | "
                f"Marks: {marks}"
            )
    else:
        print("No matching student found.")

    connection.close()



def update_student():
    print("Update Student (type q to cancel)")

    # Get student ID
    while True:
        id_input = get_input("Enter student ID: ")

        if id_input is None:
            return

        try:
            student_id = int(id_input)

            if student_id > 0:
                break
            else:
                print("Student ID must be positive.")

        except ValueError:
            print("Please enter a valid number.")

    # Get new marks
    while True:
        marks_input = get_input("Enter new marks (0-100): ")

        if marks_input is None:
            return

        try:
            new_marks = int(marks_input)

            if 0 <= new_marks <= 100:
                break
            else:
                print("Marks must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")

    # Update database only after all inputs are valid
    connection = sqlite3.connect("student_management.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET marks = ?
        WHERE id = ?
    """, (new_marks, student_id))

    connection.commit()

    if cursor.rowcount > 0:
        print("Student updated successfully.")
    else:
        print("Student not found.")

    connection.close()




def delete_student():
    print("Delete Student (type q to cancel)")

    # Get student ID
    while True:
        id_input = get_input("Enter student ID to delete: ")

        if id_input is None:
            return

        try:
            student_id = int(id_input)

            if student_id > 0:
                break
            else:
                print("Student ID must be greater than 0.")

        except ValueError:
            print("Please enter a valid number.")

    connection = sqlite3.connect("student_management.db")
    cursor = connection.cursor()

    # Check whether the student exists
    cursor.execute("""
        SELECT id, name
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    if student is None:
        print("Student not found.")
        connection.close()
        return

    print(f"Student selected: ID {student[0]}, Name: {student[1]}")

    # Ask for confirmation
    confirmation = get_input(
        "Delete this student? (yes/no, or q to cancel): "
    )

    if confirmation is None:
        connection.close()
        return

    if confirmation.lower() == "yes":
        cursor.execute("""
            DELETE FROM students
            WHERE id = ?
        """, (student_id,))

        connection.commit()
        print("Student deleted successfully.")

    else:
        print("Deletion cancelled.")

    connection.close()



def sort_students_by_marks():
    connection = sqlite3.connect("student_management.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, age, course, marks
        FROM students
        ORDER BY marks DESC
    """)

    students = cursor.fetchall()

    if students:
        print("\n===== Students Ranked by Marks =====")

        for student in students:
            student_id, name, age, course, marks = student

            print(
                f"ID: {student_id} | "
                f"Name: {name} | "
                f"Age: {age} | "
                f"Course: {course} | "
                f"Marks: {marks}"
            )
    else:
        print("No students found.")

    connection.close()


def student_statistics():
    connection = sqlite3.connect("student_management.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            AVG(marks),
            MAX(marks),
            MIN(marks)
        FROM students
    """)

    result = cursor.fetchone()

    total_students, average_marks, highest_marks, lowest_marks = result

    print("\n===== Student Statistics =====")
    print(f"Total students: {total_students}")

    if total_students > 0:
        print(f"Average marks: {average_marks:.2f}")
        print(f"Highest marks: {highest_marks}")
        print(f"Lowest marks: {lowest_marks}")
    else:
        print("No student marks available.")

    connection.close()




def filter_students_by_course():
    course = get_input("Enter course to filter (or q to cancel): ")

    if course is None:
        return

    if not course:
        print("Course cannot be empty.")
        return

    connection = sqlite3.connect("student_management.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, age, course, marks
        FROM students
        WHERE course LIKE ?
        ORDER BY name ASC
    """, (f"%{course}%",))

    students = cursor.fetchall()

    if students:
        print(f"\n===== Students in {course} =====")

        for student in students:
            student_id, name, age, course, marks = student

            print(
                f"ID: {student_id} | "
                f"Name: {name} | "
                f"Age: {age} | "
                f"Course: {course} | "
                f"Marks: {marks}"
            )
    else:
        print("No students found in that course.")

    connection.close()



def filter_students_by_result():
    connection = sqlite3.connect("student_management.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, age, course, marks
        FROM students
        ORDER BY marks DESC
    """)

    students = cursor.fetchall()

    if not students:
        print("No students found.")
        connection.close()
        return

    print("\n===== Student Results =====")

    for student in students:
        student_id, name, age, course, marks = student

        if marks >= 40:
            result = "PASS"
        else:
            result = "FAIL"

        print(
            f"ID: {student_id} | "
            f"Name: {name} | "
            f"Course: {course} | "
            f"Marks: {marks} | "
            f"Result: {result}"
        )

    connection.close()



def export_students_to_csv():
    csv_file = get_input(
        "Enter export filename (default: students_export.csv, or q to cancel): "
    )

    if csv_file is None:
        return

    if not csv_file:
        csv_file = "students_export.csv"

    connection = sqlite3.connect("student_management.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, age, course, marks
        FROM students
        ORDER BY id ASC
    """)

    students = cursor.fetchall()
    connection.close()

    if not students:
        print("No students available to export.")
        return

    try:
        with open(
            csv_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.writer(file)

            writer.writerow(["ID", "Name", "Age", "Course", "Marks"])
            writer.writerows(students)

        print(f"Students exported successfully to {csv_file}")

    except OSError as error:
        print(f"Could not export CSV file: {error}")






def import_students_from_csv():
    csv_file = get_input(
        "Enter CSV file path (default: students_import.csv, or q to cancel): "
    )

    if csv_file is None:
        return

    if not csv_file:
        csv_file = "students_import.csv"

    connection = None

    try:
        with open(
            csv_file,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:
            reader = csv.DictReader(file)

            required_columns = {"Name", "Age", "Course", "Marks"}

            if (
                not reader.fieldnames
                or not required_columns.issubset(reader.fieldnames)
            ):
                print("CSV file is missing required columns.")
                return

            connection = sqlite3.connect("student_management.db")
            cursor = connection.cursor()
            imported_count = 0

            for row in reader:
                name = row["Name"].strip().title()
                course = row["Course"].strip().title()

                if not name or not course:
                    raise ValueError("Name and course cannot be empty.")

                age = int(row["Age"])
                marks = int(row["Marks"])

                if not 1 <= age <= 100:
                    raise ValueError(f"Invalid age for {name}.")

                if not 0 <= marks <= 100:
                    raise ValueError(f"Invalid marks for {name}.")

                cursor.execute("""
                    INSERT INTO students (name, age, course, marks)
                    VALUES (?, ?, ?, ?)
                """, (name, age, course, marks))

                imported_count += 1

            connection.commit()
            print(f"Successfully imported {imported_count} students.")

    except FileNotFoundError:
        print("CSV file not found.")

    except (KeyError, ValueError) as error:
        if connection:
            connection.rollback()
        print(f"Import failed: {error}. No records were imported.")

    except sqlite3.Error as error:
        if connection:
            connection.rollback()
        print(f"Database error: {error}. Import cancelled.")

    finally:
        if connection:
            connection.close()


            







def main():
    create_database()

    while True:
        print("\n===== Student Management System =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        print("7. Sort Students by Marks")
        print("8. Student Statistics")
        print("9. Filter Students by Course")
        print("10. Filter Students by Result")
        print("11. Export Students to CSV")
        print("12. Import Students from CSV")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            print("Goodbye!")
        
        elif choice == "7":
            sort_students_by_marks()

        elif choice == "8":
            student_statistics()
            

        elif choice == "9":
            filter_students_by_course()

        elif choice == "10":
            filter_students_by_result()


        elif choice == "11":
            export_students_to_csv()

        elif choice == "12":
            import_students_from_csv()
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()