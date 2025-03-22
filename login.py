import sqlite3
from tkinter import *
import tkinter.messagebox
import os  # To execute external Python files

# SQLite Database setup
def setup_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Create users table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)
    # Insert default admin user if not exists
    cursor.execute("""
    INSERT OR IGNORE INTO users (username, password, role) VALUES
    ('admin', 'admin123', 'Admin')
    """)
    conn.commit()
    conn.close()

# Validate login credentials
def validate_login():
    username = username_var.get()
    password = password_var.get()
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()

    if result:
        role = result[0]
        tkinter.messagebox.showinfo("Login Successful", f"Welcome, {role}!")
        login_window.destroy()  # Close the login window
        if role == "Admin":
            open_admin_dashboard()
        elif role == "Student":
            open_student_dashboard()
    else:
        tkinter.messagebox.showerror("Login Failed", "Invalid Username or Password")
    conn.close()

# Open Admin Dashboard
def open_admin_dashboard():
    admin_window = Tk()
    admin_window.title("Admin Dashboard")
    admin_window.geometry("400x300")
    admin_window.configure(bg="#f0f8ff")

    Label(admin_window, text="Welcome to Admin Dashboard", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=20)
    
    # Button to launch the library management system
    def open_library_system():
        try:
            os.system("python library.py")  # Run the library.py file
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"Failed to open library system: {str(e)}")
    
    Button(admin_window, text="Open Lib-hub", command=open_library_system, font=("Arial", 14), bg="#5cb85c", fg="white").pack(pady=10)
    Button(admin_window, text="Close", command=admin_window.destroy, font=("Arial", 14), bg="#d9534f", fg="white").pack(pady=10)
    admin_window.mainloop()

# Open Student Dashboard
def open_student_dashboard():
    student_window = Tk()
    student_window.title("Student Dashboard")
    student_window.geometry("400x300")
    student_window.configure(bg="#eaf7ff")

    Label(student_window, text="Welcome to Student Dashboard", font=("Arial", 16, "bold"), bg="#eaf7ff").pack(pady=20)
    
    # Button to launch the student management system
    def open_student_system():
        try:
            os.system("python student.py")  # Run the student.py file
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"Failed to open student system: {str(e)}")
    
    Button(student_window, text="Open Lib-Hub", command=open_student_system, font=("Arial", 14), bg="#0275d8", fg="white").pack(pady=10)
    Button(student_window, text="Close", command=student_window.destroy, font=("Arial", 14), bg="#d9534f", fg="white").pack(pady=10)
    student_window.mainloop()

# Open Registration Window
def open_registration_window():
    registration_window = Toplevel(login_window)
    registration_window.title("Student Registration")
    registration_window.geometry("350x250")
    registration_window.configure(bg="#fef8e6")
    
    # Variables for registration inputs
    reg_username_var = StringVar()
    reg_password_var = StringVar()
    
    # Registration form
    Label(registration_window, text="Username:", font=("Arial", 14), bg="#fef8e6").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    Entry(registration_window, textvariable=reg_username_var, font=("Arial", 14)).grid(row=0, column=1, padx=10, pady=10)
    
    Label(registration_window, text="Password:", font=("Arial", 14), bg="#fef8e6").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    Entry(registration_window, textvariable=reg_password_var, show="*", font=("Arial", 14)).grid(row=1, column=1, padx=10, pady=10)
    
    # Register button
    def register_student():
        username = reg_username_var.get()
        password = reg_password_var.get()
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'Student')", (username, password))
            conn.commit()
            tkinter.messagebox.showinfo("Success", "Student registered successfully!")
            registration_window.destroy()
        except sqlite3.IntegrityError:
            tkinter.messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        finally:
            conn.close()
    
    Button(registration_window, text="Register", command=register_student, font=("Arial", 14), bg="#5bc0de", fg="white").grid(row=2, column=0, columnspan=2, pady=20)

# Login Window
login_window = Tk()
login_window.title("Login System")
login_window.geometry("400x300")
login_window.configure(bg="#f0f8ff")

# Variables for login inputs
username_var = StringVar()
password_var = StringVar()

# Login form
Label(login_window, text="Username:", font=("Arial", 14), bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=10, sticky="w")
Entry(login_window, textvariable=username_var, font=("Arial", 14)).grid(row=0, column=1, padx=10, pady=10)

Label(login_window, text="Password:", font=("Arial", 14), bg="#f0f8ff").grid(row=1, column=0, padx=10, pady=10, sticky="w")
Entry(login_window, textvariable=password_var, show="*", font=("Arial", 14)).grid(row=1, column=1, padx=10, pady=10)

Button(login_window, text="Login", command=validate_login, font=("Arial", 14), bg="#5cb85c", fg="white").grid(row=2, column=0, pady=20)
Button(login_window, text="Register as Student", command=open_registration_window, font=("Arial", 14), bg="#0275d8", fg="white").grid(row=2, column=1, pady=20)

# Configure the grid
login_window.grid_rowconfigure(0, weight=1)
login_window.grid_rowconfigure(1, weight=1)
login_window.grid_rowconfigure(2, weight=1)
login_window.grid_columnconfigure(0, weight=1)
login_window.grid_columnconfigure(1, weight=1)

# Setup Database
setup_database()

# Start Login Loop
login_window.mainloop()
