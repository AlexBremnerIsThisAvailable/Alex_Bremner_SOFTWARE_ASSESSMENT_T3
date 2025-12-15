from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) 

DATABASE_FILE = 'LoginData.db' 

def get_posts():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row 
    posts = conn.execute("SELECT * FROM POSTS ORDER BY timestamp DESC").fetchall()
    conn.close()
    return posts

def get_all_users():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    users = conn.execute("SELECT * FROM USERS WHERE Username != 'Admin'").fetchall()
    conn.close()
    return users



@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    Username = request.form.get('username') 
    password = request.form.get('password')
    connection = sqlite3.connect(DATABASE_FILE) 
    cursor = connection.cursor()
    

    user_record = cursor.execute("SELECT Username, role FROM USERS WHERE Username = ? AND password = ?", (Username, password)).fetchone()
    connection.close()

    if user_record:
     
        logged_in_user = user_record[0] 
        user_role = user_record[1] 
        

        return redirect(f'/home?status=logged_in&user={logged_in_user}&role={user_role}')
    else: 
        return redirect(url_for('login')) 

@app.route('/home')
def home():
    username = request.args.get('user')
    role = request.args.get('role')

    if not username:
         return redirect(url_for('login'))

    posts = get_posts() 
    return render_template('home.html', username=username, posts=posts, role=role)

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
        cursor.execute("INSERT INTO USERS (Username, password, role) VALUES (?, ?, ?)", (Username, password, 'User'))
        connection.commit()
        return redirect(f'/home?status=logged_in&user={Username}&role=User')
    except sqlite3.IntegrityError:
        connection.rollback()
        return redirect(url_for('signup'))
    finally:
        connection.close()

@app.route('/create_post', methods=['POST'])
def create_post():
    post_content = request.form.get('content')
    username = request.args.get('user', 'Anonymous') 
    role = request.args.get('role')

    if post_content and username:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO POSTS (username, content) VALUES (?, ?)", (username, post_content))
        conn.commit()
        conn.close()
    
    return redirect(f'/home?status=logged_in&user={username}&role={role}')

@app.route('/delete_post', methods=['POST'])
def delete_post():
    post_id = request.form.get('post_id')
    current_user_deleting = request.args.get('user')
    current_user_role = request.args.get('role')

    if post_id and current_user_deleting:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        if current_user_role == 'Admin':
            cursor.execute("DELETE FROM POSTS WHERE id = ?", (post_id,))
        else:
            cursor.execute("DELETE FROM POSTS WHERE id = ? AND username = ?", (post_id, current_user_deleting))
            
        conn.commit()
        conn.close()
    
    return redirect(f'/home?status=logged_in&user={current_user_deleting}&role={current_user_role}')




@app.route('/adminhome')
def adminhome():
    role = request.args.get('role')
    user = request.args.get('user')
    
    if role != 'Admin':
        abort(403) 

    users = get_all_users()
    return render_template('adminhome.html', users=users, user=user, role=role) 

@app.route('/admin_change_role', methods=['POST'])
def admin_change_role():
    role = request.args.get('role')
    user = request.args.get('user')

    if role != 'Admin': abort(403)

    target_user = request.form.get('username')
    new_role = request.form.get('new_role')

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE USERS SET role = ? WHERE Username = ?", (new_role, target_user))
    conn.commit()
    conn.close()

    return redirect(f'/adminhome?user={user}&role={role}')

@app.route('/admin_delete_account', methods=['POST'])
def admin_delete_account():
    role = request.args.get('role')
    user = request.args.get('user')

    if role != 'Admin': abort(403)

    target_user = request.form.get('username')

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM POSTS WHERE username = ?", (target_user,))
    cursor.execute("DELETE FROM USERS WHERE Username = ?", (target_user,))
    conn.commit()
    conn.close()

    return redirect(f'/adminhome?user={user}&role={role}')


if __name__ == '__main__':
    app.run(debug=True)
