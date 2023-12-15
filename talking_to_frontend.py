from flask import Flask, render_template, request, redirect, url_for
import oracledb

from flask import session
from user_class import User
from post_class import Post


app = Flask(__name__)
app.secret_key = 'goodbye_world'

oracledb.init_oracle_client(lib_dir=r"C:\app\Adam\product\21c\cfgtoollogs\dbca\dbhomeXE\bin")

db_username = 'actual_db_username' 
db_password = 'actual_db_password'  
dsn = 'actual_host:port/service_name'  

@app.route('/', methods=['GET'])
def home():
    # Render the login page initially
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    form_username = request.form.get('username')
    form_password = request.form.get('password')

    try:
        with oracledb.connect(user=db_username, password=db_password, dsn=dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT count(*) FROM your_users_table WHERE username = :1 AND password = :2"
            cursor.execute(query, [form_username, form_password])
            (user_count,) = cursor.fetchone()
            if user_count > 0:
                # User credentials are correct, so set the username in the session
                session['username'] = form_username
                # Redirect to the main page upon successful login
                return redirect(url_for('main_page'))
            else:
                # If the credentials are wrong, inform the user
                return 'Invalid username or password'
    except oracledb.Error as e:
        print("Error connecting to Oracle DB", e)
        return 'Database connection failed'
    except Exception as e:
        print("An error occurred:", e)
        return 'An error occurred during login'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')  # Hash this password!
        age = request.form.get('age')

        # Create a new User object
        new_user = User(username, email, password, age)

        # Insert the new user into the database
        try:
            with oracledb.connect(user=db_username, password=db_password, dsn=dsn) as connection:
                cursor = connection.cursor()
                insert_query = "INSERT INTO users_table (username, email, password, age) VALUES (:1, :2, :3, :4)"
                cursor.execute(insert_query, [new_user.get_username(), new_user.get_email(), new_user.get_password(), new_user.get_age()])
                connection.commit()
                return 'Registration successful!'
        except oracledb.Error as e:
            print("Error connecting to Oracle DB", e)
            return 'Registration failed'
    else:
        return render_template('register.html')
    
@app.route('/create_post', methods=['POST'])
def post():
    # Ensure the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    # Retrieve the user ID from the username in the session
    user_id = get_user_id_from_username(session['username'])
    if user_id is None:
        return 'User not found', 404

    # Get the data from the form
    data = request.form.get('data')

    # Create a new Post object
    new_post = Post(user_id, data)

    # Insert the new post into the database
    try:
        with oracledb.connect(user=db_username, password=db_password, dsn=dsn) as connection:
            cursor = connection.cursor()
            insert_query = "INSERT INTO posts_table (user_id, time, data) VALUES (:1, CURRENT_TIMESTAMP, :2)"
            cursor.execute(insert_query, [new_post.get_user_id(), new_post.get_data()])
            connection.commit()
            return 'Post successful!'
    except oracledb.Error as e:
        print("Error connecting to Oracle DB", e)
        return 'Post failed', 500
    
def get_user_id_from_username(username):
    try:
        with oracledb.connect(user=db_username, password=db_password, dsn=dsn) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM your_users_table WHERE username = :1", [username])
            result = cursor.fetchone()
            return result[0] if result else None
    except oracledb.Error as e:
        print(f"Error fetching user ID for username {username}: {e}")
        return None

@app.route('/main', methods=['GET'])
def main_page():
    # Serve the main content page
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
