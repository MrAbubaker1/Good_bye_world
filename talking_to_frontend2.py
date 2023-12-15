from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
import os
import threading
import sqlite3

from flask import flash

thread_local = threading.local()

template_dir = os.path.abspath('Frontend/HTML')
static_dir = os.path.abspath('Frontend')
print('Template directory is set to:', template_dir)
print('Static directory is set to:', static_dir)

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.secret_key = 'goodbye_world'

# Create and connect to SQLite database
db_filename = 'Eatup.db'
db_conn = sqlite3.connect(db_filename)
db_cursor = db_conn.cursor()

# Create tables if they don't exist
db_cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    age INTEGER
)''')

db_cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    post_content TEXT,
    post_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)''')
db_conn.commit()


def get_connection():
    if not hasattr(thread_local, 'connection'):
        thread_local.connection = sqlite3.connect('Eatup.db')  # Create a new connection for this thread
    return thread_local.connection


@app.route('/', methods=['GET'])
def home():
    # Check if user is logged in
    if 'username' in session:
        # User is logged in, render the main index page
        return render_template('index.html')
    else:
        # User is not logged in, render the login page
        return render_template('login.html')
    
@app.route('/login', methods=['POST'])
def login():
    error = None
    form_username = request.form.get('username')
    form_password = request.form.get('password')

    try:
        connection = get_connection()  # Get the thread-specific connection
        cursor = connection.cursor()

        cursor.execute("SELECT password FROM users WHERE username = ?", (form_username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]
            if bcrypt.checkpw(form_password.encode('utf-8'), stored_password.encode('utf-8')):
                session['username'] = form_username
                return redirect(url_for('home'))

        error = 'Invalid username or password'

    except sqlite3.Error as e:
        print("SQLite error:", e)
        error = 'Database connection failed'

    except Exception as e:
        print("An error occurred:", e)
        error = 'An error occurred during login'

    finally:
        cursor.close()  # Close the cursor
        return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        dob = request.form.get('dob')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        connection = get_connection()  # Use the thread-local connection
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            existing_username = cursor.fetchone()
            
            if existing_username:
                return render_template("create_account.html", error="Username already exists. Please choose a different username.")
            
            cursor.execute("INSERT INTO users (username, email, password, age) VALUES (?, ?, ?, ?)",
                           (username, email, hashed_password, dob))
            connection.commit()
            print('Redirecting to thank you page')
            return redirect(url_for('thank_you_template'))

        except sqlite3.Error as e:
            flash(f"SQLite error: {e}", 'error')
            print("SQLite error:", e)  # This will print to the console
            return render_template("create_account.html", error="Registration failed. Please try again.")
        finally:
            cursor.close()
    else:
        flash('Please fill in the registration form.', 'info')
        return render_template("create_account.html")


@app.route('/thank_you_template')
def thank_you_template():
    return render_template("thank_you.html")

@app.route('/create_post', methods=['POST'])
def post():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = get_user_id_from_username(session['username'])
    if user_id is None:
        return 'User not found'

    data = request.form.get('data')

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO posts (user_id, post_content) VALUES (?, ?)",
                      (user_id, data))
        connection.commit()
        return 'Post successful!'
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return 'Post failed', 500
    finally:
        cursor.close()


def get_user_id_from_username(username):
    try:
        db_cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        result = db_cursor.fetchone()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"SQLite error fetching user ID for username {username}: {e}")
        return None

@app.teardown_appcontext
def close_connection(exception=None):
    connection = getattr(thread_local, 'connection', None)
    if connection is not None:
        connection.close()


if __name__ == '__main__':
    app.run(debug=True)
