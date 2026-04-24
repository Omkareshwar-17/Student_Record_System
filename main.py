#Student_Records
FILE_NAME = "Student_Records.txt"

def menu():
    print("\n---------Student Records Management System---------")
    print("1. Add Students")
    print("2. View All Students")
    print("3. Search Students by SAP ID")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Show Passed Students")
    print("7. Show Failed Students")
    print("8. Sort Students By Marks")
    print("9. Show Topper")
    print("10. Count Topper")
    print("11. Save Records To File")
    print("12. Load Students From File")
    print("13. Exit")

def add_student(students):
    print("\n------Add Student-----")
    roll = int(input("Enter Sap ID: "))
    name = input("Enter Name: ")
    age = int(input("Enter age: "))
    course = input("Enter Course: ")
    marks = float(input("Enter CGPA: "))
#used marks for making it easy 
    found = False
    for s in students:
        if s["roll"] == roll:
            found = True
            break
    
    if found:
        print("Student with this roll no. already exists")
    else:
        student = {
            "roll" : roll,
            "name" : name,
            "age" : age,
            "course" : course,
            "marks" : marks
        }
        students.append(student)
        print("Student Added Succesfully")

def show_students(students):
    print("\n-------All Students-------")
    if len(students) == 0:
        print("No Student Records Found")
    else:
        for s in students:
            print("Sap ID:", s["roll"])
            print("Name:", s["name"])
            print("Age:", s["age"])
            print("Course:", s["course"])
            print("CGPA:", s["marks"])
            print("_______________________________")

def search_student(students):
    found = False
    roll = int(input("Enter SAP ID to Search: "))
    for s in students:
      
        if s["roll"] == roll:
            print("Student Found")
            print("Sap ID:", s["roll"])
            print("Name:", s["name"])
            print("Age:", s["age"])
            print("Course:", s["course"])
            print("CGPA:", s["marks"])
            found = True
            break
    if found == False:
            print("No records found with this SAP ID")

def update_student(students):
    print("\n------ Update Student-------")
    roll = int(input("Enter SAP Id to update: "))
    found = False

    for s in students:
        if s["roll"] == roll:
            print("Current Details")
            print("Sudent Found")
            print("Sap ID:", s["roll"])
            print("Name:", s["name"])
            print("Age:", s["age"])
            print("Course:", s["course"])
            print("CGPA:", s["marks"])

            print("Enter New Details")

            s["name"] = (input("Name: "))
            s["age"] = int(input("Age: "))
            s["course"] = input("Course: ")
            s["marks"] = float(input("CGPA: "))

            print("Students Records Updated")

            found = True
            break
    if found == False:
            print("Student Not Found")
        
def delete_student(students):
    print("\n-------Delete Student--------")
    roll = int(input("Enter SAP ID to delete: "))
    found = False

    for s in students:
        if s["roll"] == roll:
            students.remove(s)
            print("Student details deleted succefully")
            found = True
            break
    if not found:
        print("Student Not Found")

def show_passed_students(students):
    print("\n-----Passed Students------")
    passed_students = []

    for s in students:
        if s["marks"] >= 3.5:
            passed_students.append(s)

    if len(passed_students) == 0:
        print("No student Passed")
    else:
        for s in passed_students:
            print("SAP", s["roll"], "Name", s["name"], "CGPA", s["marks"])

def show_failed_students(students):
    print("\n-----Passed Students------")
    failed_students = []

    for s in students:
        if s["marks"] < 3.5:
            failed_students.append(s)

    if len(failed_students) == 0:
        print("No student Failed")
    else:
        for s in failed_students:
            print("SAP", s["roll"], "Name", s["name"], "CGPA", s["marks"])

def sort_students_by_marks(students):
    print("\n-----Sort Students By Marks-------")
    if len(students) == 0:
        print("no students records available")
    else:
        sorted_students = sorted(students, key=lambda x: x["marks"], reverse = True)

        for s in sorted_students:
            print("SAP", s["roll"], "Name", s["name"], "CGPA", s["marks"])

def show_topper(students):
    print("\n-------Topper-------")
    if len(students) == 0:
        print("No Records Found")
    else:
        topper = students[0]

    for s in students:
        if s["marks"] > topper["marks"]:
            topper = s
    print("Topper Details:")
    print("SAP ID:", topper["roll"])
    print("Name:", topper["name"])
    print("Age:", topper["age"])
    print("Course:", topper["course"])
    print("CGPA:", topper["marks"])

def count_students(students):
    print("\n----- Total Students -----")
    print("Total number of students =", len(students))

def save_to_file(students):
    print("\n----- Save Records -----")
    file = open(FILE_NAME, "w")

    for s in students:
        record = str(s["roll"]) + "|" + s["name"] + "|" + str(s["age"]) + "|" + s["course"] + "|" + str(s["marks"]) + "\n"
        file.write(record)

    file.close()
    print("Records saved to file successfully.")


def load_from_file(students):
    print("\n----- Load Records -----")
    students.clear()

    file = open(FILE_NAME, "r")
    lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line != "":
            data = line.split("|")

            student = {
                "roll": int(data[0]),
                "name": data[1],
                "age": int(data[2]),
                "course": data[3],
                "marks": float(data[4])
            }

            students.append(student)

    file.close()
    print("Records loaded from file successfully.")



def main():
    students = []

    while True:
        menu()
        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_student(students)

        elif choice == 2:
            show_students(students)

        elif choice == 3:
            search_student(students)

        elif choice == 4:
            update_student(students)

        elif choice == 5:
            delete_student(students)

        elif choice == 6:
            show_passed_students(students)

        elif choice == 7:
            show_failed_students(students)

        elif choice == 8:
            sort_students_by_marks(students)

        elif choice == 9:
            show_topper(students)

        elif choice == 10:
            count_students(students)

        elif choice == 11:
            save_to_file(students)

        elif choice == 12:
            load_from_file(students)

        elif choice == 13:
            print("Thank you for using Student Record Management System.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 13.")

main()
