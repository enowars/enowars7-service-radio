from flask import (
    Flask,
    render_template_string,
    send_file,
    request,
    session,
    redirect,
    url_for,
)
from flask_cors import CORS, cross_origin
import validator
import os
import database_manager
from html_container import html_container
import secrets
import sqlite3
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
import re

# Start app.
app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*", "methods": ["POST"]}})

# Define the upload folder.
app.config["UPLOAD_FOLDER"] = "UPLOAD_FOLDER"


database_manager.create_database()

# Set a secret key for the app
app.secret_key = secrets.token_hex()

login_manager = LoginManager()
login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_name):
    # Connect to the SQLite database
    conn = sqlite3.connect("proposals.db")

    # Create a new table with two columns
    conn.execute(
        """CREATE TABLE IF NOT EXISTS user
             (id NUMBER,
            username TEXT,
             password TEXT)"""
    )
    conn = sqlite3.connect("proposals.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username=?", (user_name,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        user = User(user_data[0], user_data[1], user_data[2])
        return user
    else:
        return None


# Only allow usernames which are 30 letters long
def validate_username(username):
    pattern = r"^[a-zA-Z]{1,30}$"
    return re.match(pattern, username) is not None and len(username) > 1


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            username = request.form["email"]
            password = request.form["password"]
        except:
            return "invalid login try"

        conn = sqlite3.connect("proposals.db")
        # Create a new table with two columns
        conn.execute(
            """CREATE TABLE IF NOT EXISTS user
                (id TEXT,
                username TEXT,
                password TEXT)"""
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username=?", (username,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data and len(user_data) == 3 and user_data[2] == password:
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login")), 400

    return render_template_string(
        """
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               <p> You don't have an account yet? Click here:</p>
               <a href="/register">Sign up</a>
               """
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
        except:
            return "invalid register data"
        # validate username
        if not validate_username(username):
            return "Bad username"

        conn = sqlite3.connect("proposals.db")

        # Create a new table with two columns
        conn.execute(
            """CREATE TABLE IF NOT EXISTS user
                ( id NUMBER,
                username TEXT,
                password TEXT)"""
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username=?", (username,))
        user_data = cursor.fetchone()

        if user_data:
            return "Username already exists. Please choose a different username."
        else:
            # ID number 1 is the readonly permisson
            cursor.execute(
                "INSERT INTO user (id, username, password) VALUES (?,?,?)",
                (username, username, password),
            )
            conn.commit()
            conn.close()

            return 'Registration successful. Please <a href="/login">login</a> to access the app.'

    return render_template_string(
        """<!DOCTYPE html>
<html>
<head>
    <title>Registration</title>
</head>
<body>
    <h2>Registration</h2>
    <form action="/register" method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br><br>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>

        <input type="submit" value="Register">
    </form>
</body>
</html>
"""
    )


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return "Logged out"


@login_manager.unauthorized_handler
def unauthorized_handler():
    return "Unauthorized", 401


# Home page
@app.route("/home", methods=["GET", "POST"])
@cross_origin()
@login_required
def home():
    html_con = html_container()
    if request.method == "GET":
        try:
            query = request.args.get("search")
            artist = database_manager.search_artist_by_title(query)
            return html_con.show_search_result(artist, query)
        except:
            return html_con.set_title_and_artist(None, None, None)
    # Else read-in song and validate it and play.
    try:
        uploaded_file = request.files["mp3-file"]
    except:
        return "Bad File, no mp3-file", 404
    # Save the file to disk
    filename = current_user.username + ".mp3"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    uploaded_file.save(filepath)
    # Validate MP3 and get metadata if valid. Else empty array.
    meta_data = validator.get_metadata(filepath)
    # No valide meta data was found.
    if meta_data == []:
        os.remove(filepath)
        return "Bad File, no artist or title or Techno song", 404
    # No techno artsit or song name is longer than
    if len(meta_data[0]) > 100 or len(meta_data[1]) > 100:
        return "Bad File, artist or/ and title to long, max 200 characters", 404
    # Play uploaded song
    return render_template_string(
        html_con.set_title_and_artist(
            meta_data[1], meta_data[0], current_user.username
        ).replace("#", "")
    )
    """try:
        return render_template_string(
            html_con.set_title_and_artist(
                meta_data[1], meta_data[0], current_user.username
            ).replace("#", "")
        )
    except:
        return (
            html_con.set_title_and_artist(
                "DUMMY_TITLE", "DUMMY_ARTIST", current_user.username
            ),
            400,
        )"""


# Give access to uploaded file
@app.route("/UPLOAD_FOLDER/<path:file_path>")
@cross_origin()
@login_required
def get_uploaded_file(file_path):
    username, ext = os.path.splitext(file_path)
    if ext.lower() == ".mp3" and username == current_user.username:
        # If no file exists there is nothing to be send here
        if not os.path.exists("UPLOAD_FOLDER/" + file_path):
            return "No file", 400
        return send_file("UPLOAD_FOLDER/" + file_path)
    else:
        return "No permission to see that file", 401
