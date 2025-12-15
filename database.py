import sqlite3

connection = sqlite3.connect('LoginData.db')
cursor = connection.cursor()


cmd1 = """ CREATE TABLE IF NOT EXISTS USERS (Username varchar(50) primary key,
                                        password varchar(50) not null) """

cursor.execute(cmd1)


cmd2 = """ INSERT INTO USERS (Username, password) values ('tester', 'tester1') """

try:
    cursor.execute(cmd2)
    connection.commit()
    print("Default user 'tester' created with a plain text password.")
except sqlite3.IntegrityError:
    print("User 'tester' already exists. Rolling back commit.")
    connection.rollback()

ans = cursor.execute("select * from USERS").fetchall()
print("\nCurrent database users:")
for i in ans:
    print(i)

connection.close()
