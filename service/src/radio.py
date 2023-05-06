import pyaudio
import requests
import sqlite3

conn = sqlite3.connect()
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS ")

stream_url = "https://streams.kqed.org/kqedradio"  # replace with the actual stream URL

chunk_size = 1024  # number of bytes to read at a time
audio_format = pyaudio.paInt16  # audio format (16-bit signed integer)
channels = 2  # stereo
sample_rate = 44100  # sample rate (Hz)

p = pyaudio.PyAudio()
stream = requests.get(stream_url, stream=True)


def callback(in_data, frame_count, time_info, status):
    data = stream.read(chunk_size)
    return (data, pyaudio.paContinue)


stream = p.open(
    format=audio_format,
    channels=channels,
    rate=sample_rate,
    output=True,
    stream_callback=callback,
)

stream.start_stream()

while stream.is_active():
    pass

stream.stop_stream()
stream.close()
p.terminate()
