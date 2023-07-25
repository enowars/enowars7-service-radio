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
import datetime
import schedule

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

    return render_template_string(html_container.login_html)


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
            save_profile_to_database(username, "", "")
            return redirect(url_for("login"))

    return render_template_string(html_container.register_html)


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return "Logged out. Go back to <a href='/login'>login</a> page"


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
    # No techno artsit or song name is longer than 91 characters
    if len(meta_data[0]) > 91 or len(meta_data[1]) > 91:
        return "Bad File, artist or/ and title to long, max 91 characters", 404
    # Play uploaded song

    return render_template_string(
        html_con.set_title_and_artist(
            meta_data[1], meta_data[0], current_user.username
        ).replace("#", "")
    )


# User profile page
@app.route("/about_<username>", methods=["GET", "POST"])
@cross_origin()
@login_required
def profile(username):
    if request.method == "GET":
        if current_user.username.lower() != username.lower():
            return "Not authorized", 401
        # load profile
        data = get_profile_from_database(username)
        return render_template_string(
            html_container.profile_html,
            username=current_user.username,
            bio=data[0],
            festivals=data[1],
        )
    if request.method == "POST":
        if current_user.username != username:
            return "Not authorized", 401
        bio = request.form["bio"]
        festivals = request.form["festivals"]
        save_profile_to_database(current_user.username, bio, festivals)
        # load profile
        data = get_profile_from_database(username)
        return render_template_string(
            html_container.profile_html,
            username=current_user.username,
            bio=data[0],
            festivals=data[1],
        )


# Redirect to profile page
@app.route("/aboutme")
@login_required
def redirect_to_own_profile():
    return redirect(f"about_{current_user.username}")


# Show history of Thunderwave radio
@app.route("/history")
@login_required
def history():
    return html_container.history_html


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


# Profile page set function
def save_profile_to_database(username, bio, festivals):
    conn = sqlite3.connect("proposals.db")
    c = conn.cursor()

    c.execute(
        "CREATE TABLE IF NOT EXISTS profiles (username TEXT, bio TEXT, festivals TEXT)"
    )
    # Check if the profile already exists in the database
    c.execute("SELECT username FROM profiles WHERE username=?", (username,))
    existing_username = c.fetchone()

    if existing_username:
        # If the profile exists, update the existing row
        c.execute(
            "UPDATE profiles SET bio=?, festivals=? WHERE username=?",
            (bio, festivals, username),
        )
    else:
        # If the profile doesn't exist, insert a new row
        c.execute(
            "INSERT INTO profiles (username, bio, festivals) VALUES (?, ?, ?)",
            (username, bio, festivals),
        )

    conn.commit()
    conn.close()


# Profile page get function
def get_profile_from_database(username):
    conn = sqlite3.connect("proposals.db")
    cursor = conn.cursor()

    cursor.execute("SELECT bio, festivals FROM profiles WHERE username=?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data


# Delete files older than 30 min
def delete_old_files(folder_path):
    import subprocess

    command = ["find", folder_path, "-type", "f", "-mmin", "+30", "-delete"]
    subprocess.run(command, check=True)


# Define the function to be scheduled
def schedule_delete_files():
    folder_path = "UPLOAD_FOLDER"
    delete_old_files(folder_path)


# Schedule the function to run every 5 minutes
def run_scheduler():
    import threading

    threading.Timer(60 * 5, run_scheduler).start()  # Schedule the next run in 5 minutes
    schedule_delete_files()


# Start the scheduler
run_scheduler()
