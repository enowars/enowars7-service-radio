from flask import Flask, send_file, render_template, request
from flask_cors import CORS, cross_origin
import validator
import os
import database_manager
import html_container

# Start app.
app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*", "methods": ["POST"]}})
# Define the upload folder.
app.config["UPLOAD_FOLDER"] = "UPLOAD_FOLDER"

database_manager.create_database()


@app.route("/", methods=["GET", "POST"])
@cross_origin()
def home():
    # If normal get just show home site
    if request.method == "GET":
        return html_container.set_title_and_artist(None, None)
    # Else read-in song and validate it and play. TODO change
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
    # Play uploaded song
    return html_container.set_title_and_artist(meta_data[0], meta_data[1])


@app.route("/UPLOAD_FOLDER/<path:file_path>")
@cross_origin()
def get_uploaded_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext.lower() == ".mp3":
        return send_file("UPLOAD_FOLDER/" + file_path)
    else:
        return send_file("UPLOAD_FOLDER/Tomer.mp3")


@app.route("/resources/image")
@cross_origin()
def get_icon():
    return send_file("resources/thunderTechno.png")
