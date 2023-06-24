import socket
import time
from lms_database import *
import pickle

HEADER=64
PORT=1234
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
FORMAT='utf-8'
DISCONNECT_MESSAGE='!DISCONNECT'

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

server.listen()

   # now our endpoint knows about the OTHER endpoint.
client, address = server.accept()
print(f"Connection from {address} has been established.")

ack=0

while ack==0:
   username=client.recv(1024).decode()
   password=client.recv(1024).decode()    

   #check if the values match in the database

   login=verify_user(username,password)

   client.send(login.encode())

   ack=int(client.recv(1024).decode())

while True:
    choice=int(client.recv(1024).decode())
 
    match choice:
        case 1:
            book_list=view_books_all()
            client.send(pickle.dumps(book_list))

        case 2:
            book_id=int(client.recv(1024).decode())
            if book_id == -1:
                continue
            response=issue(username,book_id)
            client.send(response.encode())

        case 3:
            client.send(deposit(username).encode())

        case 4:
            user_details=view_users(username)
            client.send(pickle.dumps(user_details))

        case 5:
            late_fee = pay_fee(username)
            if late_fee == 0:
                msg = "No fee to be paid."
            else:
                msg = "Fees paid succesfully"
            client.send(msg.encode())

        case default:
            pass

client.close()