import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

filename = "students.json"

def load_students():
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as file:
        return json.load(file)

def save_students(students):
    with open(filename, "w") as file:
        json.dump(students, file, indent=4)

def clear_fields():
    for entry in entries.values():
        entry.config(state="normal")
        entry.delete(0, tk.END)

def add_student():
    student = {key: entry.get().strip() for key, entry in entries.items()}
    if not student["Student ID"] or not student["Name"]:
        messagebox.showwarning("Input Error", "Student ID and Name are required.")
        return
    students = load_students()
    for s in students:
        if s["Student ID"] == student["Student ID"]:
            messagebox.showerror("Duplicate", "Student ID already exists.")
            return
    students.append(student)
    save_students(students)
    messagebox.showinfo("Success", "Student added successfully.")
    clear_fields()
    refresh_table()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    students = load_students()
    for student in students:
        values = [student.get(field, "") for field in fields]
        tree.insert("", "end", values=values)

def delete_student():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select", "Please select a record to delete.")
        return
    
    # Get the Student ID from the selected row (assuming it's the first column)
    sid = tree.item(selected)["values"][0]
    if not sid:
        messagebox.showerror("Error", "Could not find Student ID of selected record.")
        return
    
    # Confirm before deleting
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student ID {sid}?")
    if not confirm:
        return
    
    students = load_students()
    # Filter out the student to delete
    students = [s for s in students if s.get("Student ID") != sid]
    save_students(students)
    messagebox.showinfo("Deleted", f"Student ID {sid} deleted successfully.")
    refresh_table()
    clear_fields()

def search_students():
    query = search_entry.get().lower()
    for row in tree.get_children():
        tree.delete(row)
    for student in load_students():
        if query in student["Student ID"].lower() or query in student["Name"].lower():
            values = [student.get(field, "") for field in fields]
            tree.insert("", tk.END, values=values)

def load_selected():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select", "Please select a record to load.")
        return
    values = tree.item(selected)["values"]
    for i, field in enumerate(fields):
        entries[field].config(state="normal")
        entries[field].delete(0, tk.END)
        entries[field].insert(0, values[i])
    entries["Student ID"].config(state="disabled")

def update_record():
    sid = entries["Student ID"].get()
    if not sid:
        messagebox.showwarning("Error", "Load a record first.")
        return
    students = load_students()
    updated = False
    for student in students:
        if student["Student ID"] == sid:
            for key in fields:
                if key != "Student ID":
                    student[key] = entries[key].get()
            updated = True
            break
    if updated:
        save_students(students)
        messagebox.showinfo("Updated", "Record updated successfully.")
        clear_fields()
        refresh_table()
    else:
        messagebox.showerror("Error", "Student ID not found.")

def update_single_fields():
    sid = entries["Student ID"].get().strip()
    if not sid:
        messagebox.showwarning("Input Error", "Please enter Student ID to update a record.")
        return

    students = load_students()
    updated = False
    for student in students:
        if student["Student ID"] == sid:
            for key in fields:
                if key == "Student ID":
                    continue  # Don't change Student ID
                new_value = entries[key].get().strip()
                if new_value:  # Update only if field is not empty
                    student[key] = new_value
                    updated = True
            break

    if updated:
        save_students(students)
        messagebox.showinfo("Success", "Field(s) updated successfully.")
        clear_fields()
        refresh_table()
    else:
        messagebox.showerror("Error", "Student ID not found or no fields updated.")

def filter_by_course_section():
    selected_course = course_combo.get().lower()
    selected_section = section_combo.get().lower()
    for row in tree.get_children():
        tree.delete(row)
    for student in load_students():
        course = student.get("Course", "").lower()
        section = student.get("Section", "").lower()
        if (selected_course in course) and (selected_section in section):
            values = [student.get(field, "") for field in fields]
            tree.insert("", tk.END, values=values)

def update_filter_options():
    students = load_students()
    courses = sorted(set(s.get("Course", "") for s in students))
    sections = sorted(set(s.get("Section", "") for s in students))
    course_combo["values"] = courses
    section_combo["values"] = sections

# --- GUI SETUP WITH COLORS AND TITLE ---
root = tk.Tk()
root.title("Student Records")
root.geometry("1150x720")
root.configure(bg="#2c3e50")  # Dark blue background

# Title label
title_label = tk.Label(root, text="Student Records", font=("Helvetica", 28, "bold"), fg="white", bg="#34495e", pady=15)
title_label.pack(fill="x")

# Main frame with light background
main_frame = tk.Frame(root, bg="#ecf0f1", padx=15, pady=15)
main_frame.pack(fill="both", expand=True, padx=15, pady=10)

fields = [
    "Student ID", "Roll No", "Name", "Email", "Contact",
    "Address", "DOB", "Course", "Branch", "Section", "Semester", "Year"
]

entries = {}

form_frame = ttk.LabelFrame(main_frame, text="Enter Student Details")
form_frame.configure(borderwidth=3, relief="ridge")
form_frame.pack(fill="x", pady=10)

for i, field in enumerate(fields):
    lbl = ttk.Label(form_frame, text=field)
    lbl.grid(row=i//2, column=(i%2)*2, padx=8, pady=6, sticky="w")
    entry = ttk.Entry(form_frame, width=32)
    entry.grid(row=i//2, column=(i%2)*2 + 1, padx=8, pady=6)
    entries[field] = entry

btn_frame = tk.Frame(main_frame, bg="#ecf0f1")
btn_frame.pack(pady=10)

btn_color = "#2980b9"  # blue
btn_fg = "white"
btn_active = "#3498db"

def style_button(btn):
    btn.configure(bg=btn_color, fg=btn_fg, activebackground=btn_active, relief="raised", bd=3, font=("Helvetica", 10, "bold"))
    btn.bind("<Enter>", lambda e: btn.configure(bg=btn_active))
    btn.bind("<Leave>", lambda e: btn.configure(bg=btn_color))

buttons = [
    ("Add Student", add_student),
    ("Load Selected", load_selected),
    ("Update Record", update_record),
    ("Update Single Field(s)", update_single_fields),
    ("Delete Selected", delete_student),
    ("Clear Form", clear_fields),
]

for i, (text, cmd) in enumerate(buttons):
    b = tk.Button(btn_frame, text=text, command=cmd, width=18)
    b.grid(row=0, column=i, padx=5)
    style_button(b)

search_frame = ttk.Frame(main_frame)
search_frame.pack(fill="x", pady=8)

ttk.Label(search_frame, text="Search by ID or Name:").pack(side="left", padx=5)
search_entry = ttk.Entry(search_frame, width=30)
search_entry.pack(side="left", padx=5)
ttk.Button(search_frame, text="Search", command=search_students).pack(side="left", padx=5)
ttk.Button(search_frame, text="Show All", command=refresh_table).pack(side="left", padx=5)

filter_frame = ttk.LabelFrame(main_frame, text="Filter by Course and Section")
filter_frame.pack(fill="x", pady=10)

ttk.Label(filter_frame, text="Course:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
course_combo = ttk.Combobox(filter_frame, values=[], width=30)
course_combo.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(filter_frame, text="Section:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
section_combo = ttk.Combobox(filter_frame, values=[], width=20)
section_combo.grid(row=0, column=3, padx=5, pady=5)

ttk.Button(filter_frame, text="Filter", command=filter_by_course_section).grid(row=0, column=4, padx=10)

table_frame = ttk.Frame(main_frame)
table_frame.pack(fill="both", expand=True, pady=10)

tree = ttk.Treeview(table_frame, columns=fields, show="headings")
for col in fields:
    tree.heading(col, text=col)
    tree.column(col, width=90, anchor="w")

tree.pack(fill="both", expand=True)

refresh_table()
root.mainloop()