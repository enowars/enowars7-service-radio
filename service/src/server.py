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
import html_container
import secrets
import authentication


# Start app.
app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*", "methods": ["POST"]}})
# Define the upload folder.
app.config["UPLOAD_FOLDER"] = "UPLOAD_FOLDER"
with open("../data/flag", "r") as file:
    data = file.read()
app.config["EXTRA_CONFIG"] = data
database_manager.create_database()

# TODO load from env. Set a secret key for the app
app.secret_key = "my-secret-key"

# Configure the session cookie to be secure, HttpOnly, and SameSite
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"

# TODO Remove only for testing
# Add a values to db
database_manager.add_to_database("Mobby Barley", "No SQL No crime", b"\x23\x23\x12")
database_manager.add_to_database("Mimi", "Katz", b"\x23\x23\x12")
database_manager.add_to_database("BadRabbit", "Katz", b"\x23\x23\x12")
database_manager.add_to_database(
    "Flag",
    "FindMe",
    b"\x46\x4C\x41\x47\x7B\x35\x51\x37\x5F\x31\x4E\x4A\x33\x43\x54\x31\x30\x4E\x7D",
)


@app.before_request
def require_login():
    # Check if the user is not logged in and the request is not to the login page
    if session is {} or ("userid" not in session and request.endpoint != "login"):
        # Redirect the user to the login page
        valid_user = False
        try:
            valid_user = authentication.validate_user(session["userid"])
        except:
            # return redirect(url_for("login"))
            return "PLEASE VISIT /login"
        return valid_user


@app.route("/")
def redirect_further():
    return redirect(url_for("login"))


@app.route("/login")
def login():
    # Set the username in the session
    # Generate a random hex string of 32 bytes (i.e., 256 bits)
    secret_value = secrets.token_hex(32)
    session["userid"] = authentication.register_user(secret_value)
    return redirect("http://localhost:8000/" + str(session["userid"]))


# Home page
@app.route("/<userid>", methods=["GET", "POST"])
@cross_origin()
def home(userid):
    # If normal get just show home site
    if request.method == "GET":
        try:
            query = request.args.get("search")
            artist = database_manager.search_artist_by_title(query)
            return html_container.show_search_result(artist, query)
        except:
            return html_container.set_title_and_artist(None, None)
    # Else read-in song and validate it and play.
    try:
        uploaded_file = request.files["mp3-file"]
    except:
        print("ERROR wrong upload")
        return "Bad File"
    # Save the file to disk
    filename = "tmp.mp3"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    uploaded_file.save(filepath)
    # Validate MP3 and get metadata if valid. Else empty array.
    meta_data = validator.get_metadata(filepath)
    # No valide meta data was found.
    if meta_data == []:
        os.remove(filepath)
        return "Bad File"
    # TODO do it as long as needed to exploit it
    # No techno artsit or song name is longer than XXX
    if len(meta_data[0]) > 1000 or len(meta_data[1]) > 1000:
        return "Bad File"
    # Play uploaded song
    return render_template_string(
        html_container.set_title_and_artist(meta_data[1], meta_data[0])
    )


# Give access to uploaded file
@app.route("/UPLOAD_FOLDER/<path:file_path>")
@cross_origin()
def get_uploaded_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext.lower() == ".mp3":
        return send_file("UPLOAD_FOLDER/" + file_path)
    else:
        return send_file("UPLOAD_FOLDER/Tomer.mp3")
