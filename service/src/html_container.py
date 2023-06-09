import html
import eyed3


class html_container:
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

    login_html = """<!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
    </head>
    <body>
        <h1>Login</h1>
        <form action="/login" method="POST">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <input type="submit" value="Login">
        </form>
    </body>
    </html>
    """
    blocklist_ssti = [
        "config",
        "0",
        ".os",
        ".popen",
        "sys",
        ".read",
        "2",
        "4",
        "6",
        "7",
        "5",
        "8",
        "SECRET_KEY",
        "init_",
        "globals_",
        "/passwd",
        "/",
    ]

    # Helper function to get comment
    def get_mp3_comments(self, username):
        # Open the file in binary mode.
        audio_file = eyed3.load("UPLOAD_FOLDER/" + username + ".mp3")
        if (
            audio_file is not None
            and audio_file.tag is not None
            and audio_file.tag.comments is not None
        ):
            comments = [comment.text for comment in audio_file.tag.comments]
            comment = "".join(comments)
        else:
            comment = ""
        return comment

    # Show details
    def show_detail_button(self, username):
        comment = self.get_mp3_comments(username)
        # TODO add more Tag infos
        html_template = '<h1>Show MP3 File Details</h1> <button onclick="toggleDetails()">Show Details</button> <div id="details" style="display: none;"> <p>MP3 Comment: {}</p></div><script>function toggleDetails() {{var details = document.getElementById("details");details.style.display = details.style.display === "none" ? "block" : "none";}}</script>'

        return html_template.format(comment)

    def set_title_and_artist(self, title, artist, username):
        if artist is None or title is None:
            return self.main_html + "</div>" + self.search_html + self.script_html
        else:
            # Prevent XSS attacks
            title = html.escape(title)
            artist = html.escape(artist)
            # Prevent SSTI attacks
            for b in self.blocklist_ssti:
                title = title.replace(b, "")
                artist = artist.replace(b, "")
            artist = artist.replace("+", "'")
            title = title.replace("+", "'")
            src = "UPLOAD_FOLDER/" + username + ".mp3"
            append_html = "<h2> {} </h2> <h3>by {}</h3><audio src={} autoplay controls></audio>".format(
                artist, title, src
            )
            show_detail_button_html = self.show_detail_button(username)
            return (
                self.main_html
                + "</div>"
                + append_html
                + show_detail_button_html
                + self.search_html
                + self.script_html
            )

    def show_search_result(self, artist, title):
        # If no artist found for the title return
        if artist is None:
            return (
                self.main_html
                + "</div>"
                + self.search_html
                + "<p> Nothing found!"
                + self.script_html
            )
        else:
            if len(artist) > 1:
                artist = ",".join(str(x[0]) for x in artist)
            else:
                artist = str(artist[0][0])
            return (
                self.main_html
                + "</div>"
                + self.search_html
                + "<p>Found "
                + str(title)
                + " by "
                + str(artist)
                + self.script_html
            )
