import sqlite3

connection = sqlite3.connect('LoginData.db')
cursor = connection.cursor()


cmd1 = """ CREATE TABLE IF NOT EXISTS USERS (
    Username varchar(50) primary key,
    password varchar(50) not null
) """
cursor.execute(cmd1)


cmd2 = """ INSERT OR IGNORE INTO USERS (Username, password) values (?, ?) """

cursor.execute(cmd2, ('tester', 'tester1')) 

connection.commit()

ans = cursor.execute("select * from USERS").fetchall()
print("Current database users:")
for i in ans:
    print(i)

connection.close()
