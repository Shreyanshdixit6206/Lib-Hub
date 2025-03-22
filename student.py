from tkinter import *
import tkinter.messagebox
import backend

# Initialize the main window
root = Tk()
root.title('Library Management System')
root.geometry("600x400")
root.configure(bg="#f0f8ff")  # Light blue background

# Callback for closing the app
def callback():
    if tkinter.messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

# Clear input fields
def clear():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)

# Add a new book entry
def add_entry():
    backend.insert(title_txt.get(), author_txt.get(), year_txt.get(), isbn_txt.get())
    listing.delete(0, END)
    listing.insert(END, (title_txt.get(), author_txt.get(), year_txt.get(), isbn_txt.get()))
    clear()

# View all entries
def view_all():
    listing.delete(0, END)
    for row in backend.view():
        listing.insert(END, row)
    clear()

# Update selected entry
def update():
    global selected_tuple
    backend.update(selected_tuple[0], title_txt.get(), author_txt.get(), year_txt.get(), isbn_txt.get())
    view_all()

# Select a row from the Listbox
def get_selected_row(event):
    global selected_tuple
    clear()
    index = listing.curselection()[0]
    selected_tuple = listing.get(index)
    e1.insert(END, selected_tuple[1])
    e2.insert(END, selected_tuple[2])
    e3.insert(END, selected_tuple[3])
    e4.insert(END, selected_tuple[4])

# Delete selected entry
def delete():
    global selected_tuple
    backend.delete(selected_tuple[0])
    view_all()

# Search for specific entries
def search():
    listing.delete(0, END)
    search_data = backend.search(title_txt.get(), author_txt.get(), year_txt.get(), isbn_txt.get())
    if len(search_data) != 0:
        for row in search_data:
            listing.insert(END, row)
    else:
        tkinter.messagebox.showinfo("Message", "NO RESULT FOUND")
    clear()

# Borrow a book
def borrow_book():
    student_window = Tk()
    student_window.title("Student Dashboard")
    student_window.geometry("400x300")
    student_window.configure(bg="#eaf7ff")

    Label(student_window, text="Visit library for borrowing of the book.\nYou entry have been stored.", font=("Arial", 16, "bold"), bg="#eaf7ff").pack(pady=20)
    

# Input variables
selected_tuple = tuple()
title_txt = StringVar()
author_txt = StringVar()
year_txt = StringVar()
isbn_txt = StringVar()

# Layout
Label(root, text="Title", fg="#333", bg="#f0f8ff", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
e1 = Entry(root, textvariable=title_txt, font=("Arial", 12))
e1.grid(row=0, column=1, padx=10, pady=10, sticky="we")

Label(root, text="Year", fg="#333", bg="#f0f8ff", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
e2 = Entry(root, textvariable=year_txt, font=("Arial", 12))
e2.grid(row=1, column=1, padx=10, pady=10, sticky="we")

Label(root, text="Author", fg="#333", bg="#f0f8ff", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=10, sticky="w")
e3 = Entry(root, textvariable=author_txt, font=("Arial", 12))
e3.grid(row=0, column=3, padx=10, pady=10, sticky="we")

Label(root, text="ISBN", fg="#333", bg="#f0f8ff", font=("Arial", 12)).grid(row=1, column=2, padx=10, pady=10, sticky="w")
e4 = Entry(root, textvariable=isbn_txt, font=("Arial", 12))
e4.grid(row=1, column=3, padx=10, pady=10, sticky="we")

# Buttons
button_frame = Frame(root, bg="#f0f8ff")
button_frame.grid(row=2, column=3, rowspan=6, padx=10, pady=10, sticky="nsew")

Button(button_frame, text="View All", command=view_all, font=("Arial", 12), bg="#5cb85c", fg="white").pack(fill="x", pady=5)
Button(button_frame, text="Search Entry", command=search, font=("Arial", 12), bg="#0275d8", fg="white").pack(fill="x", pady=5)
Button(button_frame, text="Borrow Book", command=borrow_book, font=("Arial", 12), bg="#f0ad4e", fg="white").pack(fill="x", pady=5)  # New Borrow button
Button(button_frame, text="Close", command=root.destroy, font=("Arial", 12), bg="#292b2c", fg="white").pack(fill="x", pady=5)

# Listbox with scrollbar
list_frame = Frame(root)
list_frame.grid(row=2, column=0, rowspan=6, columnspan=3, padx=10, pady=10, sticky="nsew")

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side=RIGHT, fill=Y)

listing = Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Arial", 12))
listing.pack(side=LEFT, fill=BOTH, expand=True)
listing.bind('<<ListboxSelect>>', get_selected_row)

scrollbar.config(command=listing.yview)

# Grid weights for responsiveness
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
for i in range(8):
    root.grid_rowconfigure(i, weight=1)

# Protocol for window close
root.protocol("WM_DELETE_WINDOW", callback)

# Run the application
root.mainloop()
