import sqlite3

connection = sqlite3.connect('LoginData.db')
cursor = connection.cursor()

cmd1 = """ CREATE TABLE IF NOT EXISTS USERS (
    Username varchar(50) primary key,
    password varchar(50) not null,
    role varchar(10) not null default 'User'
) """
cursor.execute(cmd1)


cmd3 = """ CREATE TABLE IF NOT EXISTS POSTS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
) """
cursor.execute(cmd3)


cmd2 = """ INSERT OR IGNORE INTO USERS (Username, password, role) values (?, ?, ?) """
cursor.execute(cmd2, ('tester', 'tester1', 'User')) 


cmd4 = """ INSERT OR IGNORE INTO USERS (Username, password, role) values (?, ?, ?) """
cursor.execute(cmd4, ('Admin', 'Admin', 'Admin')) 

connection.commit()

ans = cursor.execute("select * from USERS").fetchall()
print("Current database users:")
for i in ans:
    print(i)

connection.close()
