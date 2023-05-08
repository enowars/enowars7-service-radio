import eyed3
import sqlite3
import os
from eyed3.mp3.headers import isValidHeader


# Add MP3 file to playlist
def add_to_playlist(file):
    get_metadata(file)


# Read information out of MP3 file
def get_metadata(file):
    # validate that it is a MP3 file
    try:
        audio_file = eyed3.load(file)
    except:
        return []
    if validate_mp3(audio_file, file):
        if audio_file.info is not None and audio_file.tag is not None:
            # extract Artist, Title and length of song
            print(audio_file.info.time_secs)
            print(audio_file.tag.artist)
            print(audio_file.tag.title)
            return [
                audio_file.info.time_secs,
                audio_file.tag.artist,
                audio_file.tag.title,
            ]
    # Return empty array if file is not in expected format
    # or does not contain expected informations.
    return []


# Helper function
def validate_mp3_header(file_path):
    # Check if file exists
    if not os.path.exists(file_path):
        raise ValueError("File does not exist.")

    # Open the file in binary mode
    with open(file_path, "rb") as f:
        # Read the first 6 bytes (of the MP3 header)
        header = f.read(6)
        # If not at least 6 bytes provided return
        if len(header) < 6:
            return
        # Check if the header is valid
        if header[:2] != b"ID" and (0 < header[3] < 3):
            print("Wrong header")
            return False

        # Get the version and flags
        version_major = 2
        version_minor = ord(header[3:4])
        flags = ord(header[5:6])

        # Check if the version and flags are valid
        if version_major != 2 or version_minor not in [0, 1, 2, 3, 4]:
            print(
                "ID%d v%d.%d is not supported"
                % (header[3], version_major, version_minor)
            )
            return False
        if flags & 0x1F != flags:
            print("Wrong flag")
            return False

        # Print the MP3 header information
        print("Version: {}.{}".format(version_major, version_minor))
        print("Flags: {:08b}".format(flags))
        # TODO control size of file
        return True


# Validate MP3 File
def validate_mp3(audio_file, fp):
    print(
        isinstance(audio_file, eyed3.mp3.Mp3AudioFile),
        audio_file.info.mp3_header is not None,
        validate_mp3_header(fp),
    )
    return (
        isinstance(audio_file, eyed3.mp3.Mp3AudioFile)
        and audio_file.info.mp3_header is not None
        and validate_mp3_header(fp)
    )


print(get_metadata("../../exploit.mp3"))
