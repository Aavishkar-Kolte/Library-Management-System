import tkinter as tk
from tkinter import messagebox
import socket
import time
from tkinter import font
import pickle
from tkinter import ttk

HEADER = 64
PORT = 1234
SERVER = '192.168.62.74'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection_status = 0 
ack = 0



def login():
    global ack
    username = entry_username.get()
    password = entry_password.get()

    if ack == 0:
        client.send(username.encode())
        client.send(password.encode())

        verification = client.recv(1024).decode()

        if verification == "User Exists":
            ack = 1
            messagebox.showinfo("Login", "Login successful!")
            show_main_ui()
            client.send(str(ack).encode())
        else:
            ack = 0
            messagebox.showerror("Login", "Invalid username or password")
            client.send(str(ack).encode())


def connect_to_server():
    global connection_status
    if connection_status == 0:
        try:
            client.connect(ADDR)
            connection_status = 1
        except ConnectionRefusedError:
            messagebox.showerror("Login", "Could not connect to server.")



def show_login_ui():
    menu_ui.pack_forget()
    login_ui.pack()  



def show_main_ui():
    login_ui.pack_forget()
    menu_ui.pack()



def show_view_ui():
    menu_ui.pack_forget()
    for widget in view_ui.winfo_children():
        widget.destroy()
    x = 1
    client.send(str(x).encode())
    book_list=client.recv(1024)
    books=pickle.loads(book_list)
    tree = ttk.Treeview(view_ui)
    tree["columns"] = ("Name", "Status")
    tree.heading("#0", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Status", text="Status")
    tree.column("#0", width=50)
    tree.column("Name", width=200)
    tree.column("Status", width=100)

    tk.Label(view_ui,text="Library Management System", font=Label_font).pack()
    tk.Label(view_ui, height=2).pack()
    
    for x in books:
        y = (x[0],x[2])
        tree.insert(parent="", index="end", text=x[1], values=y)
        tree.pack()

    tk.Label(view_ui, height=2).pack()
    tk.Button(view_ui, text="back", command=back_to_menu,height=1,width=10).pack()
    view_ui.pack()




def show_profile_ui():
    menu_ui.pack_forget()

    for widget in profile_ui.winfo_children():
        widget.destroy()
    

    x = 4
    client.send(str(x).encode())
    temp = client.recv(1024)
    user=pickle.loads(temp)

    tk.Label(profile_ui,text="Library Management System", font=Label_font).pack()
    tk.Label(profile_ui, height=2).pack()
    tk.Label(profile_ui, text=f"Username: {user[0]}", height=2).pack()
    tk.Label(profile_ui, text=f"Password: {user[1]}", height=2).pack()

    if(user[2]!=None):
        tk.Label(profile_ui, text=f"Book issued: {user[2]}(ID: {user[3]})",height=2).pack()
        tk.Label(profile_ui, text=f"Issue date: {user[4]}",height=2).pack()
        tk.Label(profile_ui, text=f"Due date: {user[5]}",height=2).pack()
        tk.Label(profile_ui, text=f"Late fees: {user[6]}",height=2).pack()
        tk.Label(profile_ui, height=2).pack()
        tk.Button(profile_ui, text="Pay late fees",command=pay_late_fee).pack()
    else:
        tk.Label(profile_ui, text=f"Late fees: {user[6]}",height=2).pack()
        tk.Label(profile_ui, text="No Book is issued.",height=2).pack()
        tk.Label(profile_ui, height=2).pack()
        tk.Button(profile_ui, text="Pay late fees",command=pay_late_fee).pack()

    tk.Label(profile_ui, height=2).pack()
    tk.Button(profile_ui, text="back", command=back_to_menu,height=1,width=10).pack()   
    profile_ui.pack()


def pay_late_fee():
    x = 5
    client.send(str(x).encode())
    msg = client.recv(1024)
    messagebox.showinfo("deposit", msg )

def show_issue_ui():
    menu_ui.pack_forget()
    login_ui.pack_forget()
    x = 2
    client.send(str(x).encode())
    issue_ui.pack()

def issue_book(id):
    client.send(str(id).encode())
    msg = client.recv(1024)
    messagebox.showinfo("issue", msg)



def show_deposit_ui():
    x = 3
    client.send(str(x).encode())
    msg = client.recv(1024)
    messagebox.showinfo("deposit", msg )


def back_to_menu():
    menu_ui.pack_forget()
    profile_ui.pack_forget()
    view_ui.pack_forget()
    deposit_ui.pack_forget()
    menu_ui.pack()


def issue_back_to_menu():
    menu_ui.pack_forget()
    profile_ui.pack_forget()
    view_ui.pack_forget()
    issue_ui.pack_forget()
    deposit_ui.pack_forget()
    x = -1
    client.send(str(x).encode())
    menu_ui.pack()

def issue(book):
    if book != '':
        issue_book(book)

window = tk.Tk()
window.title("LMS")
window.geometry("500x420")
Label_font = font.Font(family="Arial",size=14)

login_ui = tk.Frame(window)
menu_ui= tk.Frame(window)
view_ui = tk.Frame(window)
issue_ui = tk.Frame(window)
deposit_ui = tk.Frame(window)
profile_ui = tk.Frame(window)






# Login UI
tk.Label(login_ui, height=2).pack()
tk.Label(login_ui,text="Library Management System", font=Label_font).pack()
tk.Label(login_ui, height=2).pack()
tk.Label(login_ui, text="Username").pack()
entry_username = tk.Entry(login_ui)
entry_username.pack()
tk.Label(login_ui, text="Password").pack()
entry_password = tk.Entry(login_ui, show="*")
entry_password.pack()
s1 = tk.Label(login_ui, text=" ")
s1.pack()
button = tk.Button(login_ui, text="Login", command=login)
button.pack()




# Menu UI
tk.Label(menu_ui,text="Library Management System", font=Label_font).pack()
tk.Label(menu_ui, height=2).pack()
tk.Button(menu_ui, text="Profile",command=show_profile_ui,width=12,height=2).pack()
tk.Label(menu_ui, height=2).pack()
tk.Button(menu_ui, text="View books", command=show_view_ui,width=12,height=2,).pack()
tk.Label(menu_ui, height=2).pack()
tk.Button(menu_ui, text="Issue", command=show_issue_ui,width=12,height=2).pack()
tk.Label(menu_ui, height=2).pack()
tk.Button(menu_ui, text="Deposit",command=show_deposit_ui,width=12,height=2).pack()


# Issue UI
tk.Label(issue_ui,text="Library Management System", font=Label_font).pack()
tk.Label(issue_ui, height=2).pack()
tk.Label(issue_ui, text="Enter book ID").pack()
book_id = tk.Entry(issue_ui)
book_id.pack()
tk.Label(issue_ui, height=2).pack()
tk.Button(issue_ui, text="issue book", command=lambda: issue(book_id.get()),height=1,width=10).pack()
tk.Label(issue_ui, height=2).pack()
tk.Button(issue_ui, text="back", command=issue_back_to_menu,height=1,width=10).pack()



if connection_status == 0:
    connect_to_server()


show_login_ui()

window.mainloop()













