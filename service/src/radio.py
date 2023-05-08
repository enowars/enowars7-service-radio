import vlc

# Create instance of VLC player
instance = vlc.Instance("--no-xlib")

# Create new Media Player object
player = instance.media_player_new()

# Define list of radio station URLs and names TODO add some more
radio_stations = [
    {
        "name": "News",
        "url": "http://kcrw.streamguys1.com/kcrw_192k_mp3_on_air_internet_radio",
    },
    {"name": "Something", "url": "http://strm112.1.fm/acountry_mobile_mp3"},
    {
        "name": "Techno",
        "url": "https://regiocast.streamabc.net/regc-90s90stechno2195701-mp3-192-2408420",
    },
    {"name": "Dutch", "url": "http://icecast.omroep.nl/3fm-bb-mp3"},
    {
        "name": "Pokemon",
        "url": "https://d3ctxlq1ktw2nl.cloudfront.net/staging/2021-02-22/076cb4bb38331a52417f0317d1ef07a9.m4a",
    },
]

# Display list of radio stations and prompt user to select one
print("Choose a radio station:")
for i, station in enumerate(radio_stations):
    print(f'{i + 1}. {station["name"]}')
selection = int(input()) - 1

# Set selected radio station as the media to be played by the player
media = instance.media_new(radio_stations[selection]["url"])
player.set_media(media)

# Start playback
player.play()

# Wait for playback to finish
while True:
    pass
