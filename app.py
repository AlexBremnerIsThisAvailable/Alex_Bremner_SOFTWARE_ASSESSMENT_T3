from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

app.secret_key = os.urandom(24) 

DATABASE_FILE = 'LoginData.db' 

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    Username = request.form.get('username') 
    password = request.form.get('password')
  
    connection = sqlite3.connect(DATABASE_FILE) 
    cursor = connection.cursor()
  

    user_records = cursor.execute("SELECT * FROM USERS WHERE Username = ? AND password = ?", (Username, password)).fetchall()
    connection.close()

    if len(user_records) > 0:

        user_data = user_records[0]

        return redirect(f'/home?username={user_data[0]}&password={user_data[1]}')
    else: 
        return redirect(url_for('login'))

@app.route('/home')
def home():

    username = request.args.get('username')
    password = request.args.get('password')
    

    return render_template('home.html', username=username, password=password)

@app.route('/signup')
def signup():
    return render_template('signup.html') 

@app.route('/add_user', methods=['POST'])
def add_user():
    Username = request.form.get('username')
    password = request.form.get('password')
    
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    try:

        cursor.execute("INSERT INTO USERS (Username, password) VALUES (?, ?)", (Username, password))
        connection.commit()
        

        return redirect(f'/home?username={Username}&password={password}')

    except sqlite3.IntegrityError:
        connection.rollback()
        return redirect(url_for('signup'))
        
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(debug=True)
