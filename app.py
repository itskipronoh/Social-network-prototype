from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def sqlite_version():
    connection = sqlite3.connect('social-network.db')  # Replace 'mydatabase.db' with your database file
    cursor = connection.cursor()
    cursor.execute('SELECT sqlite_version()')

    version = cursor.fetchone()[0]

    connection.close()
    return f'SQLite Version: {version}'

# Initialize the SQLite database
conn = sqlite3.connect('social_network.db', check_same_thread=False)
conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()

# Define route for the homepage
@app.route('/')
def home():
    conn = sqlite3.connect('social_network.db')
    cur = conn.cursor()
    cur.execute('SELECT p.id, p.content, p.timestamp, u.username FROM posts p JOIN users u ON p.user_id = u.id ORDER BY p.timestamp DESC')
    posts = cur.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# Define route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('social_network.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('register.html')

# Define route for creating posts
@app.route('/post', methods=['POST'])
def post():
    content = request.form['content']
    conn = sqlite3.connect('social_network.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO posts (user_id, content) VALUES (?, ?)', (1, content))  # Hardcoded user_id for simplicity
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
