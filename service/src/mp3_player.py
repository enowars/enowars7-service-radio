from pydub import AudioSegment
from pydub.playback import play
import threading


def play_mp3(mp3_path):
    audio = AudioSegment.from_file(mp3_path, format="mp3")
    play(audio)


def play_mp3_threaded(mp3_path):
    thread = threading.Thread(target=play_mp3, args=(mp3_path,))
    thread.start()


mp3_path = "../../Tomer.mp3"
play_mp3_threaded(mp3_path)
