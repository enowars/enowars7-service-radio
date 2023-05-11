from flask import Flask, send_file, render_template, request
from flask_cors import CORS, cross_origin
import validator
import os

# Start app.
app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*", "methods": ["POST"]}})
# Define the upload folder.
app.config["UPLOAD_FOLDER"] = "UPLOAD_FOLDER"


@app.route("/", methods=["GET", "POST"])
@cross_origin()
def home():
    # If normal get just show home site
    if request.method == "GET":
        return render_template("play_own_music.html")
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
        print("" + meta_data[0])
        return "Bad File"
    # Play uploaded song.
    return render_template(
        "play_own_music.html",
        mp3file={
            "filename": meta_data[1],
            "author": meta_data[0],
            "url": filepath,
        },
    )


# Route for playing radio.
@app.route("/technoRadio", methods=["GET"])
def radio():
    return "https://regiocast.streamabc.net/regc-90s90stechno2195701-mp3-192-2408420"


@app.route("/UPLOAD_FOLDER/tmp.mp3")
@cross_origin()
def get_uploaded_file():
    return send_file("UPLOAD_FOLDER/tmp.mp3")
