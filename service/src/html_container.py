""" This file contains all html parts that need to returned"""

main_html = """<!DOCTYPE html>
<html>
<style>
    .cycle {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        animation: spin 2s linear infinite paused;
    }

    .cycle::before,
    .cycle::after {
        content: "";
        width: 50%;
        height: 100%;
        position: absolute;
        top: 0;
        border-radius: 50%;
    }

    .cycle::before {
        left: 0;
        background-color: red;
        transform: translateX(-50%);
    }

    .cycle::after {
        right: 0;
        background-color: blue;
        transform: translateX(50%);
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }

        100% {
            transform: rotate(360deg);
        }
    }

    .play {
        animation-play-state: running;
    }

    .pause {
        animation-play-state: paused;
    }

    body {
        font-family: Arial, sans-serif;
        background-color: #171717;
        color: #fff;
        text-align: center;
    }

    header {
        padding: 20px;
        background-color: #4e4e4e;
        text-align: center;
    }

    h1 {
        margin: 0;
        font-size: 48px;
    }

    .container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }

    .player {
        margin: 20px;
    }

    .now-playing {
        margin: 20px;
    }

    h2 {
        margin-top: 0;
        font-size: 24px;
    }

    audio {
        width: 100%;
        max-width: 500px;
        margin: 0 auto;
        display: block;
    }

    footer {
        background-color: #4e4e4e;
        padding: 20px;
        text-align: center;
    }
</style>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Techno Radio</title>
    <link rel="stylesheet" href="styles.css">
</head>

<body>
    <header>
        <h1>Techno Radio </h1>
    </header>

    <body>
        <div>
            <p>Techno Radio Station. To listen to our livestream please click the button</p>
            <br>
            <br>
            <div class="cycle" style="text-align: center;"></div>
            <button id="play-btn" onclick="playOrPause()">Play</button>
            <video id="my-video" width="640" height="360">
                <source src="https://regiocast.streamabc.net/regc-90s90stechno2195701-mp3-192-2408420">
            </video>
            <br>
            <div
                style="background-color: #4e4e4e; padding: 20px; box-shadow: 0px 0px 10px #666666; font-family: Arial, sans-serif; font-size: 16px; color: #FFFFFF; text-align: center;">
                <h1>Submit your Proposal.</h1>
                <p> Please note we only accept Techno mp3 files!</p>
                <form method="POST" enctype="multipart/form-data">
                    <input type="file" name="mp3-file" accept="audio/mp3">
                    <input type="submit" value="Upload">
                </form>"""
search_html = """
            <h1>Search through already accepted proposals</h1>
            <form method="GET">
                <input type="text" name="search" placeholder="Search for Song Titles...">
                <input type="submit" value="Search">
            </form>
            <br>
            <br>
            <br>
            <h2>Search Results:</h2>
"""
script_html = """
        </div>
        <script>
            var video = document.getElementById("my-video");
            var button = document.getElementById("play-btn");
            const cycle = document.querySelector(".cycle");
            let isPlaying = false;

            function playOrPause() {
                if (video.paused) {
                    video.play();
                    button.innerHTML = "Pause";
                    toggleCycle()
                } else {
                    video.pause();
                    toggleCycle()
                    button.innerHTML = "Play";
                }
            }
            // Start or stop animation according to play button value.
            function toggleCycle() {
                if (isPlaying) {
                    cycle.classList.remove("play");
                    cycle.classList.add("pause");
                    isPlaying = false;
                } else {
                    cycle.classList.remove("pause");
                    cycle.classList.add("play");
                    isPlaying = true;
                }
            }
        </script>
    </body>

</html>"""


# Function that sets the pieces together and adds artist and title.
def set_title_and_artist(title, artist):
    if artist is None or title is None:
        return main_html + "</div>" + search_html + script_html
    else:
        append_html = (
            "<h2>"
            + title
            + "</h2>"
            + "<h3>by "
            + artist
            + "</h3>"
            + "<audio src=UPLOAD_FOLDER/tmp.mp3 autoplay controls></audio>"
        )
        return main_html + append_html + search_html + script_html


def show_search_result(artist, title):
    # If no artist found for the title return
    if artist is None:
        return main_html + "</div>" + search_html
    else:
        if len(artist) > 1:
            artist = ",".join(str(x[0]) for x in artist)
        else:
            artist = str(artist[0][0])
        return (
            main_html
            + "</div>"
            + search_html
            + "<p>Found "
            + str(title)
            + " by "
            + str(artist)
            + script_html
        )
