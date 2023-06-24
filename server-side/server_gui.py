import socket
import time
import pickle
from lms_database import *
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import ttk


def show_all_books_ui():
    menu_ui.pack_forget()
    for widget in all_books_ui.winfo_children():
        widget.destroy()
    tk.Label(all_books_ui, text="Library Management System Server", font=Label_font).pack()
    tk.Label(all_books_ui, height=2).pack()
    books = view_books_all()

    tree = ttk.Treeview(all_books_ui)
    tree["columns"] = ("Name", "Status")
    tree.heading("#0", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Status", text="Status")
    tree.column("#0", width=50)
    tree.column("Name", width=200)
    tree.column("Status", width=100)

    
    for x in books:
        y = (x[0],x[2])
        tree.insert(parent="", index="end", text=x[1], values=y)
        tree.pack()

    tk.Label(all_books_ui, height=2).pack()
    tk.Button(all_books_ui, text="back", command=back,height=1,width=10).pack()
    all_books_ui.pack()

def add_the_book(book_name):
    if book_name != '':
        msg = add_book(book_name)
        messagebox.showinfo("Done",msg)


def show_add_book_ui():
    menu_ui.forget()
    add_book_ui.pack()
   

def delete_the_book(book_id):
    if book_id != '':
        msg = delete_book(book_id)
        messagebox.showinfo("Done",msg)


def show_delete_book_ui():
    menu_ui.pack_forget()
    delete_book_ui.pack()


def show_all_users_ui():
    menu_ui.pack_forget()
    for widget in all_users_ui.winfo_children():
        widget.destroy()
    users = view_users_all()

    tree = ttk.Treeview(all_users_ui)
    tree["columns"] = ("Username", "Password")
    tree.heading("#0", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")
    tree.column("#0", width=50)
    tree.column("Username", width=200)
    tree.column("Password", width=100)

    tk.Label(all_users_ui, text="Library Management System Server", font=Label_font).pack()
    tk.Label(all_users_ui, height=2).pack()
    
    i = 1

    for x in users:
        y = (x[0],x[1])
        tree.insert(parent="", index="end",text=i, values=y)
        i = i+1
        tree.pack()

    tk.Label(all_users_ui, height=2).pack()
    tk.Button(all_users_ui, text="back", command=back,height=1,width=10).pack()
    all_users_ui.pack()

def add_the_user(username,password):
    if username != '' and password != '':
        msg = add_user(username, password)
        messagebox.showinfo("Done",msg)

def show_add_user_ui():
    menu_ui.pack_forget()
    add_user_ui.pack()



def delete_the_user(user_name):
    if user_name != '':
        msg = delete_user(user_name)
        messagebox.showinfo("Done",msg)


def show_delete_user_ui():
    menu_ui.pack_forget()
    delete_user_ui.pack()



def back():
    all_books_ui.pack_forget()
    all_users_ui.pack_forget()
    add_book_ui.pack_forget()
    delete_book_ui.pack_forget()
    delete_user_ui.pack_forget()
    add_user_ui.pack_forget()
    menu_ui.pack()



window = tk.Tk()
window.title("LMS Server")
window.geometry("500x400")
Label_font = font.Font(family="Arial", size=14)

menu_ui = tk.Frame(window)
all_books_ui = tk.Frame(window)
all_users_ui = tk.Frame(window)
add_book_ui = tk.Frame(window)
add_user_ui = tk.Frame(window)
delete_book_ui = tk.Frame(window)
delete_user_ui = tk.Frame(window)

# menu UI
tk.Label(menu_ui, height=2).grid(row=0,columnspan=2)
tk.Label(menu_ui, text="Library Management System Server", font=Label_font).grid(row=1,columnspan=2)
tk.Label(menu_ui, height=2).grid(row=2,columnspan=2)

tk.Button(menu_ui, text="Show all books", width=12, height=2,command=show_all_books_ui).grid(row=3, column=0, pady=10)
tk.Button(menu_ui, text="Add a new book", width=12, height=2,command=show_add_book_ui).grid(row=4, column=0, pady=10)
tk.Button(menu_ui, text="Delete a book", width=12, height=2,command=show_delete_book_ui).grid(row=5, column=0, pady=10)

tk.Button(menu_ui, text="Show all users", width=12, height=2,command=show_all_users_ui).grid(row=3, column=1, pady=10)
tk.Button(menu_ui, text="Add a new user", width=12, height=2,command=show_add_user_ui).grid(row=4, column=1, pady=10)
tk.Button(menu_ui, text="Delete a user", width=12, height=2,command=show_delete_user_ui).grid(row=5, column=1, pady=10)


#Add a new book ui
tk.Label(add_book_ui, text="Library Management System Server", font=Label_font).pack()
tk.Label(add_book_ui, height=2).pack()
tk.Label(add_book_ui, text="Enter the book name").pack()
book_name = tk.Entry(add_book_ui)
book_name.pack()
tk.Label(add_book_ui, height=2).pack()
tk.Button(add_book_ui, text="Add book", command=lambda: add_the_book(book_name.get()),height=1,width=10).pack()
tk.Label(add_book_ui, height=2).pack()
tk.Button(add_book_ui, text="back", command=back,height=1,width=10).pack()


#Delete book ui
tk.Label(delete_book_ui, text="Library Management System Server", font=Label_font).pack()
tk.Label(delete_book_ui, height=2).pack()
tk.Label(delete_book_ui, text="Enter the book ID").pack()
book_id = tk.Entry(delete_book_ui)
book_id.pack()
tk.Label(delete_book_ui, height=2).pack()
tk.Button(delete_book_ui, text="Delete book", command=lambda: delete_the_book(book_id.get()),height=1,width=10).pack()
tk.Label(delete_book_ui, height=2).pack()
tk.Button(delete_book_ui, text="back", command=back,height=1,width=10).pack()




#Add user ui
tk.Label(add_user_ui, text="Library Management System Server", font=Label_font).pack()
tk.Label(add_user_ui, height=2).pack()
tk.Label(add_user_ui, text="Username").pack()
username = tk.Entry(add_user_ui)
username.pack()
tk.Label(add_user_ui, text="Password").pack()
password = tk.Entry(add_user_ui,show='*')
password.pack()
tk.Label(add_user_ui, height=2).pack()
tk.Button(add_user_ui, text="Add user", command=lambda: add_the_user(username.get(),password.get()),height=1,width=10).pack()
tk.Label(add_user_ui, height=2).pack()
tk.Button(add_user_ui, text="back", command=back,height=1,width=10).pack()




#Delete user ui
tk.Label(delete_user_ui, text="Library Management System Server", font=Label_font).pack()
tk.Label(delete_user_ui, height=2).pack()
tk.Label(delete_user_ui, text="Enter Username").pack()
user_name = tk.Entry(delete_user_ui)
user_name.pack()
tk.Label(delete_user_ui, height=2).pack()
tk.Button(delete_user_ui, text="Delete user", command=lambda: delete_the_user(user_name.get()),height=1,width=10).pack()
tk.Label(delete_user_ui, height=2).pack()
tk.Button(delete_user_ui, text="back", command=back,height=1,width=10).pack()


menu_ui.pack()
window.mainloop()

