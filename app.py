from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'password')")
    c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (2, 'alice', '123456')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template_string('''
        <h2>Login (Vulnerable Version)</h2>
        <form method="POST" action="/login">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # 漏洞：字符串拼接
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print(f"[DEBUG] Executing query: {query}")
    c.execute(query)
    user = c.fetchone()
    conn.close()
    
    if user:
        return f"Login successful! Welcome {user[1]}."
    else:
        return "Login failed! Invalid username or password."

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8081, debug=True)