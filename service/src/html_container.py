import html
import eyed3


class html_container:
    history_html = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thunderwave Radio</title>
    <style>
        body {
            background-color: #333;
            color: #fff;
            font-family: Arial, sans-serif;
            padding: 20px;
        }

        h1 {
            font-size: 32px;
            text-align: center;
            margin-bottom: 20px;
        }

        .story {
            background-color: #111;
            padding: 20px;
            border-radius: 10px;
        }

        .story p {
            margin-bottom: 15px;
            line-height: 1.5;
        }

        .symbols {
            text-align: center;
            margin-top: 30px;
        }

        .cycle {
            display: inline-block;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            margin: 0 10px;
        }

        .blue {
            background-color: blue;
        }

        .red {
            background-color: red;
        }
    </style>
</head>

    </style>
            <style>
        body {
            margin: 0;
            padding: 0;
        }

        .navbar {
            background-color: #4e4e4e;
            padding: 20px;
        }

        .navbar ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
        }

        .navbar li {
            margin: 0 10px;
        }

        .navbar a {
            color: #fff;
            text-decoration: none;
            font-size: 18px;
            font-weight: bold;
        }

        .navbar a:hover {
            color: #ccc;
        }
    </style>
</head>

<body>
    <header class="navbar">
        <nav>
            <ul>
                <li><a href="/home">Home</a></li>
                <li><a href="/aboutme">About me</a></li>
                <li><a href="/history">History</a></li>
                <li><a href="/logout">Logout</a></li>
            </ul>
        </nav>
    </header>
    <body>

<body>
    <h1>Thunderwave Radio</h1>

    <div class="story">
        <p>Once upon a time, in the vibrant and energetic country of the Netherlands, there was a legendary event that shook the foundations of electronic music. It was the year 1997, and the world witnessed the spectacular Thunderdome music festival. The energy and enthusiasm of the crowd were palpable, as thousands of ravers came together to celebrate the pulsating beats of hardcore techno.</p>

        <p>Inspired by the overwhelming success of Thunderdome and driven by a shared passion for electronic music, a group of visionary individuals decided to embark on a new venture. They envisioned a radio station that would capture the essence of the Thunderdome experience and bring it to the airwaves. Thus, Thunderwave Radio was born.</p>

        <p>With a mission to spread the sounds of hardcore techno, Thunderwave Radio became a haven for lovers of the genre. The founders were determined to showcase not only the high-energy beats that Thunderdome was famous for but also the diverse range of electronic music styles emerging in the Netherlands and beyond.</p>

        <p>The radio station quickly gained popularity among dedicated ravers and music enthusiasts. It became a platform for talented DJs and producers to showcase their skills, with live sets, exclusive mixes, and interviews with renowned artists. As the station grew, Thunderwave Radio became a hub for discovering new talents and tracks, serving as a launchpad for aspiring artists to make their mark on the electronic music scene.</p>

        <p>The station's dedication to its listeners was unwavering. They organized exciting contests and giveaways, inviting fans to attend exclusive events and festivals. Thunderwave Radio became not only a radio station but also a community, connecting people with a shared love for the music that resonated deep within their souls.</p>

        <p>Over the years, Thunderwave Radio evolved with the changing landscape of electronic music. As new genres and subgenres emerged, the station adapted and expanded its programming, ensuring that it remained at the forefront of the electronic music scene. From classic hardcore to industrial, from trance to drum and bass, Thunderwave Radio continued to push boundaries and provide an unforgettable auditory experience.</p>

        <p>Throughout its history, Thunderwave Radio has adopted two iconic symbols that have become synonymous with the station. The blue cycle represents the rhythmic pulse of the music, symbolizing the energy and vibrancy that flows through every beat. The red cycle signifies the passion and intensity that the station and its listeners share for the music they love. These cycles have become integral parts of Thunderwave Radio's visual identity, reminding everyone of the station's rich history and the enduring power of electronic music.</p>

        <div class="symbols">
            <div class="cycle blue"></div>
            <div class="cycle red"></div>
        </div>

        <p>Today, Thunderwave Radio stands as a testament to the enduring power of music and the indomitable spirit of those who dare to dream. It remains a beacon for electronic music lovers, delivering the finest sounds and capturing the essence of the Thunderdome legacy. With each beat, Thunderwave Radio carries on the legacy of Thunderdome 1997, continuing to inspire and unite people through the magic of electronic music.</p>
    </div>
</body>

</html>
    """

    profile_html = """ <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Profile</title>
    <style>
        body {
            background-color: #000;
            color: #ccc;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }

        h1 {
            text-align: center;
            color: #ccc;
        }

        .profile-card {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #333;
            border-radius: 10px;
        }

        label {
            font-weight: bold;
        }

        textarea {
            width: 100%;
            height: 100px;
            resize: vertical;
            background-color: #ccc;
            color: #000;
            border: none;
        }

        .save-button {
            text-align: center;
            margin-top: 20px;
        }

        button {
            background-color: #000;
            color: #ccc;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #333;
        }

        p {
            margin-bottom: 10px;
        }
    </style>
            <style>
        body {
            margin: 0;
            padding: 0;
        }

        .navbar {
            background-color: #4e4e4e;
            padding: 20px;
        }

        .navbar ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
        }

        .navbar li {
            margin: 0 10px;
        }

        .navbar a {
            color: #fff;
            text-decoration: none;
            font-size: 18px;
            font-weight: bold;
        }

        .navbar a:hover {
            color: #ccc;
        }
    </style>
</head>

<body>
    <header class="navbar">
        <nav>
            <ul>
                <li><a href="/home">Home</a></li>
                <li><a href="/about_{{username}}">About me</a></li>
                <li><a href="/history">History</a></li>
                <li><a href="/logout">Logout</a></li>
            </ul>
        </nav>
    </header>
    <body>
    <script>
        function saveBio() {
            var bioTextArea = document.getElementById("bio");
            var savedBio = document.getElementById("saved-bio");
            savedBio.innerHTML = bioTextArea.value;
        }

        function saveFestivals() {
            var festivalsTextArea = document.getElementById("festivals");
            var savedFestivals = document.getElementById("saved-festivals");
            savedFestivals.innerHTML = festivalsTextArea.value;
        }
    </script>
</head>

<body>
    <h1>User Profile</h1>
    <div class="profile-card">
        <form action="/about_{{username}}" method="POST">
            <label for="username">Username:</label>
            <p id="username">{{username}}</p>

            <label for="bio">Biography:</label>
            <textarea id="bio" name="bio">{{bio}}</textarea>

            <label for="festivals">Festivals Visits:</label>
            <textarea id="festivals" name="festivals">{{festivals}}</textarea>

            <div class="save-button">
                <button type="submit">Save</button>
            </div>
        </form>
    </div>
</body>

</html>

</html>"""

    main_html = """<!DOCTYPE html>
    <html>
    <style>
        .cycle {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            position: initial;
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
        <title>Thunderwave Radio</title>
        <link rel="stylesheet" href="styles.css">
    </head>
        <style>
        body {
            margin: 0;
            padding: 0;
        }

        .navbar {
            background-color: #4e4e4e;
            padding: 20px;
        }

        .navbar ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
        }

        .navbar li {
            margin: 0 10px;
        }

        .navbar a {
            color: #fff;
            text-decoration: none;
            font-size: 18px;
            font-weight: bold;
        }

        .navbar a:hover {
            color: #ccc;
        }
    </style>
</head>

<body>
    <header class="navbar">
        <nav>
            <ul>
                <li><a href="#">Home</a></li>
                <li><a href="/aboutme">About me</a></li>
                <li><a href="/history">History</a></li>
                <li><a href="/logout">Logout</a></li>
            </ul>
        </nav>
    </header>
    <body>
        <header>
            <h1>Thunderwave Radio </h1>
        </header>

        <body>
            <div>
                <style>
                    .flex-container {
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                    }
                </style>

                <div class="flex-container">
                    <p>Thunderwave Radio Station. To listen to our livestream please click the button</p>
                    <br>
                    <div class="cycle" style="text-align: center; display: flex;"></div>
                    <br>
                    <button id="play-btn" onclick="playOrPause()">Play</button>
                    <video id="my-video" width="100" height="100">
                        <source src="https://regiocast.streamabc.net/regc-90s90stechno2195701-mp3-192-2408420">
                    </video>
                </div>
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
        "9",
        "3",
        "6",
        "7",
        "5",
        "8",
        "SECRET_KEY",
        "init_",
        "globals_",
        "/passwd",
        "_write",
        ".wrtie",
        ".read",
        ".init",
        ".globals",
    ]

    # Helper function to get comment
    def get_comments(self, username):
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
        comment = self.get_comments(username)
        # Prevent XSS attacks
        comment = html.escape(comment)
        # Prevent SSTI attacks
        for b in self.blocklist_ssti:
            comment = comment.replace(b, "")
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
