import customtkinter as ctk

# In-memory book storage
books = []

def add_book():
    title = title_var.get().strip()
    author = author_var.get().strip()
    year = year_var.get().strip()
    status = "Available"
    
    if not title or not author:
        result_label.configure(text="⚠ Title and Author required!", text_color="red")
        return
    
    books.append({"title": title, "author": author, "year": year, "status": status})
    update_list()
    result_label.configure(text="✅ Book added!", text_color="green")

def update_list():
    listbox.delete("0.0", "end")
    for b in books:
        listbox.insert("end", f"{b['title']} by {b['author']} ({b['year']}) - {b['status']}\n")

def search_book():
    query = search_var.get().strip().lower()
    listbox.delete("0.0", "end")
    for b in books:
        if query in b['title'].lower() or query in b['author'].lower():
            listbox.insert("end", f"{b['title']} by {b['author']} ({b['year']}) - {b['status']}\n")

def borrow_book():
    query = search_var.get().strip().lower()
    for b in books:
        if query in b['title'].lower() and b['status'] == "Available":
            b['status'] = "Borrowed"
            result_label.configure(text=f"📖 You borrowed '{b['title']}'", text_color="yellow")
            update_list()
            return
    result_label.configure(text="⚠ Book not available!", text_color="red")

def return_book():
    query = search_var.get().strip().lower()
    for b in books:
        if query in b['title'].lower() and b['status'] == "Borrowed":
            b['status'] = "Available"
            result_label.configure(text=f"📖 You returned '{b['title']}'", text_color="green")
            update_list()
            return
    result_label.configure(text="⚠ Book not found or already available!", text_color="red")

# Modern UI setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("📚 Library Management System")
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

app.mainloop()
