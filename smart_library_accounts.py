import sqlite3
import customtkinter as ctk

# Database setup
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year TEXT,
    status TEXT DEFAULT 'Available',
    borrowed_by INTEGER,
    FOREIGN KEY(borrowed_by) REFERENCES users(id)
)
""")
conn.commit()

# ---------------- Functions ----------------
def add_user():
    name = user_name_var.get().strip()
    email = user_email_var.get().strip()
    if not name or not email:
        result_label.configure(text="⚠ Name and Email required!", text_color="red")
        return
    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        result_label.configure(text=f"✅ User {name} added!", text_color="green")
    except sqlite3.IntegrityError:
        result_label.configure(text="⚠ Email already exists!", text_color="red")

def add_book():
    title = title_var.get().strip()
    author = author_var.get().strip()
    year = year_var.get().strip()
    if not title or not author:
        result_label.configure(text="⚠ Title and Author required!", text_color="red")
        return
    cursor.execute("INSERT INTO books (title, author, year, status) VALUES (?, ?, ?, ?)",
                   (title, author, year, "Available"))
    conn.commit()
    update_list()
    result_label.configure(text="✅ Book added!", text_color="green")

def update_list():
    listbox.delete("0.0", "end")
    cursor.execute("""
        SELECT books.title, books.author, books.year, books.status, users.name
        FROM books LEFT JOIN users ON books.borrowed_by = users.id
    """)
    for b in cursor.fetchall():
        borrower = f" - Borrowed by {b[4]}" if b[4] else ""
        listbox.insert("end", f"{b[0]} by {b[1]} ({b[2]}) - {b[3]}{borrower}\n")

def borrow_book():
    book_title = search_var.get().strip().lower()
    user_email = user_email_var.get().strip().lower()
    cursor.execute("SELECT id FROM users WHERE email=?", (user_email,))
    user = cursor.fetchone()
    if not user:
        result_label.configure(text="⚠ User not found!", text_color="red")
        return
    cursor.execute("SELECT id, title, status FROM books")
    for b in cursor.fetchall():
        if book_title in b[1].lower() and b[2] == "Available":
            cursor.execute("UPDATE books SET status=?, borrowed_by=? WHERE id=?",
                           ("Borrowed", user[0], b[0]))
            conn.commit()
            result_label.configure(text=f"📖 {user_email} borrowed '{b[1]}'", text_color="yellow")
            update_list()
            return
    result_label.configure(text="⚠ Book not available!", text_color="red")

def return_book():
    book_title = search_var.get().strip().lower()
    cursor.execute("SELECT id, title, status FROM books")
    for b in cursor.fetchall():
        if book_title in b[1].lower() and b[2] == "Borrowed":
            cursor.execute("UPDATE books SET status=?, borrowed_by=NULL WHERE id=?",
                           ("Available", b[0]))
            conn.commit()
            result_label.configure(text=f"📖 Returned '{b[1]}'", text_color="green")
            update_list()
            return
    result_label.configure(text="⚠ Book not found or already available!", text_color="red")

# ---------------- UI Setup ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("📚 Library Management System with Users")
app.geometry("700x600")

# Book input
title_var = ctk.StringVar()
author_var = ctk.StringVar()
year_var = ctk.StringVar()
search_var = ctk.StringVar()

ctk.CTkLabel(app, text="Book Title").pack(pady=5)
ctk.CTkEntry(app, textvariable=title_var).pack(pady=5)

ctk.CTkLabel(app, text="Author").pack(pady=5)
ctk.CTkEntry(app, textvariable=author_var).pack(pady=5)

ctk.CTkLabel(app, text="Year").pack(pady=5)
ctk.CTkEntry(app, textvariable=year_var).pack(pady=5)

ctk.CTkButton(app, text="Add Book", command=add_book).pack(pady=10)

# User input
user_name_var = ctk.StringVar()
user_email_var = ctk.StringVar()

ctk.CTkLabel(app, text="User Name").pack(pady=5)
ctk.CTkEntry(app, textvariable=user_name_var).pack(pady=5)

ctk.CTkLabel(app, text="User Email").pack(pady=5)
ctk.CTkEntry(app, textvariable=user_email_var).pack(pady=5)

ctk.CTkButton(app, text="Add User", command=add_user).pack(pady=10)

result_label = ctk.CTkLabel(app, text="")
result_label.pack()

# Search + borrow/return
ctk.CTkLabel(app, text="Search Book").pack(pady=5)
ctk.CTkEntry(app, textvariable=search_var).pack(pady=5)
ctk.CTkButton(app, text="Borrow Book", command=borrow_book).pack(pady=5)
ctk.CTkButton(app, text="Return Book", command=return_book).pack(pady=5)

# Book list
listbox = ctk.CTkTextbox(app, width=600, height=200)
listbox.pack(pady=10)

update_list()
app.mainloop()
