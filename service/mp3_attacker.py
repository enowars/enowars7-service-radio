import eyed3

audio_file = eyed3.load("admin.mp3")
audio_file.tag.artist = "Bratwurst"
audio_file.tag.title = "Makao"
audio_file.tag.genre = "Techno"
audio_file.tag.save()
