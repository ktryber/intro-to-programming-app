import sqlite3

db = sqlite3.connect('data/mydb')

cursor = db.cursor()

name1 = 'Andres'
phone1 = '3366858'
email1 = 'user@example.com'
password1 = '12345'
 
name2 = 'John'
phone2 = '5557241'
email2 = 'johndoe@example.com'
password2 = 'abcdef'


cursor.execute('''CREATE TABLE users(name text, phone text, email text, password text)''')

cursor.execute('''INSERT INTO users(name, phone, email, password)
                  VALUES(?,?,?,?)''', (name1,phone1, email1, password1))

db.commit()


