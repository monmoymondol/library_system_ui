import sqlite3
import customtkinter as ctk

# Database setup
conn = sqlite3.connect("library.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year TEXT,
    status TEXT DEFAULT 'Available'
)
""")
conn.commit()

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
    cursor.execute("SELECT title, author, year, status FROM books")
    for b in cursor.fetchall():
        listbox.insert("end", f"{b[0]} by {b[1]} ({b[2]}) - {b[3]}\n")

def search_book():
    query = search_var.get().strip().lower()
    listbox.delete("0.0", "end")
    cursor.execute("SELECT title, author, year, status FROM books")
    for b in cursor.fetchall():
        if query in b[0].lower() or query in b[1].lower():
            listbox.insert("end", f"{b[0]} by {b[1]} ({b[2]}) - {b[3]}\n")

def borrow_book():
    query = search_var.get().strip().lower()
    cursor.execute("SELECT id, title, status FROM books")
    for b in cursor.fetchall():
        if query in b[1].lower() and b[2] == "Available":
            cursor.execute("UPDATE books SET status=? WHERE id=?", ("Borrowed", b[0]))
            conn.commit()
            result_label.configure(text=f"📖 You borrowed '{b[1]}'", text_color="yellow")
            update_list()
            return
    result_label.configure(text="⚠ Book not available!", text_color="red")

def return_book():
    query = search_var.get().strip().lower()
    cursor.execute("SELECT id, title, status FROM books")
    for b in cursor.fetchall():
        if query in b[1].lower() and b[2] == "Borrowed":
            cursor.execute("UPDATE books SET status=? WHERE id=?", ("Available", b[0]))
            conn.commit()
            result_label.configure(text=f"📖 You returned '{b[1]}'", text_color="green")
            update_list()
            return
    result_label.configure(text="⚠ Book not found or already available!", text_color="red")

# Modern UI setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("📚 Library Management System (SQLite)")
app.geometry("600x500")

# Input fields
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

result_label = ctk.CTkLabel(app, text="")
result_label.pack()

# Search and borrow/return
ctk.CTkLabel(app, text="Search Book").pack(pady=5)
ctk.CTkEntry(app, textvariable=search_var).pack(pady=5)
ctk.CTkButton(app, text="Search", command=search_book).pack(pady=5)
ctk.CTkButton(app, text="Borrow Book", command=borrow_book).pack(pady=5)
ctk.CTkButton(app, text="Return Book", command=return_book).pack(pady=5)

# Book list
listbox = ctk.CTkTextbox(app, width=500, height=200)
listbox.pack(pady=10)

update_list()
app.mainloop()
