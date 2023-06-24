import sqlite3
from datetime import date, timedelta,datetime

conn=sqlite3.connect('library.db')

c=conn.cursor()

'''c.execute(""" CREATE TABLE books
            (
                name text,
                id integer,
                status text,
            )""")
'''
'''c.execute(""" CREATE TABLE users
            (
            id  text,
            password    text,
            issued_book_name text,
            issued_book_id  integer,
            issue_date  text,
            deposit_date    text,
            late_fee    integer
            )""")
'''

def view_books_all():
    c.execute("SELECT * FROM books ORDER BY id ASC")
    return c.fetchall()

def view_users_all():
    c.execute("SELECT * FROM USERS")
    return c.fetchall()

def view_users(username):
    c.execute("""SELECT * FROM USERS WHERE id=:username""",
              {'username':username})
    
    return c.fetchone()

def view_books(name):
    c.execute("SELECT * FROM books WHERE name=:name",{'name':name})
    print(c.fetchall())

def verify_user(username,password):

    flag=0
    c.execute("SELECT id FROM users WHERE id=:id",{'id':username})

    if(c.fetchone()==None):
        return "Incorrect Username"
    
    c.execute("SELECT password FROM users WHERE password=:password",{'password':password})
    
    if(c.fetchone()==None):
        return "Incorrect Password"
    
    return "User Exists"

def issue(username,id):

    c.execute("SELECT * FROM books WHERE id=:id",{'id':id})

    l=c.fetchone()

    if(l==None):
        return  "Book does not exist"

    if(l[2]=="Unavailable"):
        return "Book is not available for issuing"
    else:
        c.execute("""UPDATE books SET status = :status
                WHERE id = :id""",{'id': id, 'status':"Unavailable"})

        issue_date = date.today()
        deposit_date = issue_date + timedelta(weeks=2)
            
        issue_date=str(issue_date)
        deposit_date=str(deposit_date)

        c.execute("""UPDATE users SET 
                        issued_book_name=:issued_book_name,
                        issued_book_id=:issued_book_id,
                        issue_date=:issue_date,
                        deposit_date=:deposit_date 
                        WHERE id=:username""",
                        {'issued_book_name':l[0],
                         'issued_book_id':id,
                         'issue_date':issue_date,
                         'deposit_date':deposit_date,
                         'username':username
                         })
        
        conn.commit()

        return "Book Issued"
    
def deposit(username):
    c.execute("SELECT issued_book_id FROM users WHERE id=:username",{'username':username})

    book_id=c.fetchone()

    if(book_id[0]==None):
        return "User has not issued any book"
    else:
        c.execute("""UPDATE books SET status = :status
        WHERE id = :book_id""",{'book_id':book_id[0], 'status':"Available"})
        
        c.execute("""SELECT deposit_date FROM users
                        WHERE id=:username""",{'username':username})
        
        deposit_date=c.fetchone()[0]

        deposit_date = datetime.strptime(deposit_date, "%Y-%m-%d").date()

        today_date=date.today()

        num_days=(today_date-deposit_date).days

        if num_days>0:
            late_fee=num_days*2
        else:
            late_fee=0
        
        c.execute("""UPDATE users SET 
                        issued_book_name=NULL,
                        issued_book_id=NULL,
                        issue_date=NULL,
                        deposit_date=NULL,
                        late_fee=:late_fee 
                        WHERE id=:username""",
                        {'username':username,'late_fee':late_fee})

        conn.commit()

        return f'Book Deposited.\nLate fee=Rs.{late_fee}'

def pay_fee(username):
    c.execute("""SELECT late_fee FROM users
                    WHERE id=:username""",
                    {'username':username})

    late_fee=c.fetchone()[0]

    c.execute("""UPDATE users SET late_fee=0 WHERE id=:username""",
              {'username':username})

    conn.commit()
    return late_fee

def add_book(book_name):
    c.execute("SELECT MAX(id) FROM books")
    book_id=c.fetchone()[0]+1
    c.execute("""INSERT INTO books(name, id, status) 
                VALUES (:book_name,
                        :book_id,
                        'Available')"""
                        ,{'book_name':book_name,'book_id':book_id})
    conn.commit()
    return "Book added to the library"

def delete_book(book_id):
    c.execute("SELECT name FROM books WHERE id =:book_id",
              {'book_id':book_id})
    book=c.fetchone()

    if book==None:
        return f"Book with ID {book_id} does not exist"
    else:
        c.execute("DELETE FROM books WHERE id=:book_id",{'book_id':book_id})
        conn.commit()
        return "Book Removed from the Library"
    
def add_user(username,password):
    c.execute("SELECT id FROM users where id=:username",
              {'username':username})
    
    user=c.fetchone()

    if user!=None:
         return "User already exists"
    else:
        c.execute("""INSERT INTO users 
                    VALUES (:username,:password,NULL,NULL,NULL,NULL,0)""",
                    {'username':username,
                    'password':password})
        
        conn.commit()
        return "User Added"

def delete_user(username):
    c.execute("SELECT id FROM users where id=:username",
              {'username':username})
    
    if c.fetchone()!=None:
        c.execute("DELETE FROM users WHERE id=:username",
                  {'username':username})
        conn.commit()
        return "User Deleted"
    else:
        return "User Does Not Exist"

#   c.execute("""INSERT INTO books VALUES ('BB',2,'Available')""")
#   c.execute("""INSERT INTO books VALUES ('CC',3,'Available')""")
'''c.execute("""UPDATE books SET status = :status
                    WHERE id = :id""",
                  {'id': 3, 'status':"Unavailable"})'''
#c.execute("""INSERT INTO users VALUES ('21BIT01','abc',NULL,NULL,NULL,NULL,100)""")

#c.execute("DROP TABLE users")

#c.execute("""INSERT INTO books VALUES ('AA',1,'Available')""")

#c.execute("UPDATE books SET status=:status WHERE name=:name",{'name':"CC",'status':'Available'})

#c.execute("DELETE FROM books WHERE name=:name",{'name':"AA"})

#print(issue('21BIT0203',1))

#print(deposit('21BIT0203'))

#print(view_books_all())

#print(view_users_all())

#print(view_users('21BIT0203'))

#print(add_book('DD'))


#print(delete_book(4))

#print(view_books_all())

#add_user('21BIT0574','def')

#delete_user('21BIT01')

#print(view_users_all())

#print(pay_fee('21BIT01'))

conn.commit()