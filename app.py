from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) 

DATABASE_FILE = 'LoginData.db' 


def get_posts():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
 
    posts = cursor.execute("SELECT * FROM POSTS ORDER BY timestamp DESC").fetchall()
    conn.close()
    return posts

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
   
        return redirect(f'/home?status=logged_in&user={Username}')
    else: 
        return redirect(url_for('login')) 

@app.route('/home')
def home():
    username = request.args.get('user')
   
    posts = get_posts() 
 
    return render_template('home.html', username=username, posts=posts)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

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
        return redirect(f'/home?status=logged_in&user={Username}')
    except sqlite3.IntegrityError:
        connection.rollback()
        return redirect(url_for('signup'))
    finally:
        connection.close()


@app.route('/create_post', methods=['POST'])
def create_post():
   
    post_content = request.form.get('content')
   
    username = request.args.get('user', 'Anonymous') 

    if post_content:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO POSTS (username, content) VALUES (?, ?)", (username, post_content))
        conn.commit()
        conn.close()
    return redirect(f'/home?status=logged_in&user={username}') 
   

@app.route('/delete_post', methods=['POST'])
def delete_post():

    post_id = request.form.get('post_id')
    username = request.args.get('user')

    if post_id and username:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        

        cursor.execute("DELETE FROM POSTS WHERE id = ? AND username = ?", (post_id, username))
        conn.commit()
        conn.close()
    

    return redirect(f'/home?status=logged_in&user={username}')


if __name__ == '__main__':
    app.run(debug=True)


