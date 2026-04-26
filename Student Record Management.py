import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import re
from datetime import datetime

DB_NAME = "student_records.db"
BACKUP_FILE = "Student_Records_Backup.txt"

def connect_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            sap_id TEXT PRIMARY KEY,
            name TEXT, age INTEGER, course TEXT,
            semester TEXT, email TEXT, phone TEXT,
            maths INTEGER, python INTEGER, de INTEGER, 
            dsa INTEGER, physics INTEGER,
            total INTEGER, percentage REAL, grade TEXT,
            result TEXT, created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- Logic Functions ---
def validate_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

def validate_phone(phone):
    return re.match(r"^[6-9][0-9]{9}$", phone)

def calculate_grade(percentage):
    if percentage >= 75: return "A+"
    elif percentage >= 65: return "A"
    elif percentage >= 55: return "B"
    elif percentage >= 45: return "C"
    elif percentage >= 35: return "D"
    else: return "F"

def get_student_data():
    try:
        sap = sap_entry.get().strip()
        # Updated to use subject-specific entry fields
        marks = [int(maths_entry.get()), int(python_entry.get()), int(de_entry.get()), 
                 int(dsa_entry.get()), int(physics_entry.get())]
        
        if not (sap and name_entry.get().strip() and email_entry.get().strip()):
            messagebox.showerror("Error", "Required fields are empty!")
            return None
        
        if not validate_email(email_entry.get().strip()):
            messagebox.showerror("Error", "Invalid Email!")
            return None

        if not validate_phone(phone_entry.get().strip()):
            messagebox.showerror("Error", "Invalid Phone Number!")
            return None

        total = sum(marks)
        perc = total / 5
        return (sap, name_entry.get().strip(), int(age_entry.get()), course_entry.get().strip(), 
                semester_entry.get().strip(), email_entry.get().strip(), phone_entry.get().strip(),
                marks[0], marks[1], marks[2], marks[3], marks[4],
                total, perc, calculate_grade(perc), 
                "Fail" if any(m < 40 for m in marks) else "Pass",
                datetime.now().strftime("%d-%m-%Y %H:%M"))
    except ValueError:
        messagebox.showerror("Error", "Age and Marks must be numbers!")
        return None

def add_student():
    data = get_student_data()
    if data:
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
            conn.commit()
            conn.close()
            view_students()
            messagebox.showinfo("Success", "Record Added Successfully")
            clear_fields()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "SAP ID already exists!")

def update_student():
    data = get_student_data()
    if data:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""UPDATE students SET 
            name=?, age=?, course=?, semester=?, email=?, phone=?,
            maths=?, python=?, de=?, dsa=?, physics=?, total=?, 
            percentage=?, grade=?, result=?, created_at=? WHERE sap_id=?""", 
            (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], 
             data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[0]))
        conn.commit()
        conn.close()
        view_students()
        messagebox.showinfo("Success", "Record Updated")

def delete_student():
    sap = sap_entry.get().strip()
    if not sap: return
    if messagebox.askyesno("Confirm", f"Delete SAP ID {sap}?"):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE sap_id=?", (sap,))
        conn.commit()
        conn.close()
        view_students()
        clear_fields()

def search_student():
    sap = sap_entry.get().strip()
    if not sap:
        messagebox.showwarning("Warning", "Enter SAP ID to search")
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE sap_id=?", (sap,))
    row = cursor.fetchone()
    conn.close()
    if row:
        clear_fields()
        entries_to_fill = [sap_entry, name_entry, age_entry, course_entry, semester_entry, 
                           email_entry, phone_entry, maths_entry, python_entry, de_entry, 
                           dsa_entry, physics_entry]
        for i, entry in enumerate(entries_to_fill):
            entry.insert(0, row[i])
    else:
        messagebox.showerror("Error", "Student not found")

def view_students():
    for row in student_table.get_children(): student_table.delete(row)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT sap_id, name, age, course, semester, email, phone, total, percentage, grade, result FROM students")
    for row in cursor.fetchall(): student_table.insert("", tk.END, values=row)
    conn.close()

def clear_fields():
    for e in entries: e.delete(0, tk.END)

# --- GUI Setup ---
connect_database()
root = tk.Tk()
root.title("Student Management System")
root.geometry("1200x700")

tk.Label(root, text="STUDENT RECORD MANAGEMENT SYSTEM", font=("Arial", 18, "bold"), bg="navy", fg="white").pack(fill=tk.X)

f_frame = tk.Frame(root, pady=10)
f_frame.pack()

# Updated label list with specific subjects
labels = ["SAP ID", "Name", "Age", "Course", "Semester", "Email", "Phone", 
          "Maths", "Python", "Digital Electronics", "Data Structure and Algorithm", "Physics"]
entries = []
for i, label in enumerate(labels):
    tk.Label(f_frame, text=label, font=("Arial", 10)).grid(row=i//4, column=(i%4)*2, padx=5, pady=5)
    e = tk.Entry(f_frame, width=18)
    e.grid(row=i//4, column=(i%4)*2+1, padx=5, pady=5)
    entries.append(e)

# Re-mapping entry variables to the new subject names
sap_entry, name_entry, age_entry, course_entry, semester_entry, email_entry, \
phone_entry, maths_entry, python_entry, de_entry, dsa_entry, physics_entry = entries

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", width=10, bg="green", fg="white", command=add_student).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Search", width=10, command=search_student).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Update", width=10, bg="orange", command=update_student).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Delete", width=10, bg="red", fg="white", command=delete_student).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Clear", width=10, command=clear_fields).grid(row=0, column=4, padx=5)

# Treeview
t_frame = tk.Frame(root)
t_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
cols = ("SAP ID", "Name", "Age", "Course", "Sem", "Email", "Phone", "Total", "%", "Grade", "Status")
student_table = ttk.Treeview(t_frame, columns=cols, show="headings")
for col in cols: 
    student_table.heading(col, text=col)
    student_table.column(col, width=90)
student_table.pack(fill=tk.BOTH, expand=True)

def on_click(event):
    selected = student_table.focus()
    if selected:
        val = student_table.item(selected, "values")
        sap_entry.delete(0, tk.END)
        sap_entry.insert(0, val[0])
        search_student()

student_table.bind("<ButtonRelease-1>", on_click)

view_students()
root.mainloop()