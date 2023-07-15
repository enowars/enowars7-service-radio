# Service Documentation
Author: Tomer Yavor

ThunderWave is simulating an internet radio station website. With a fake history to be related to ThunderRave 1997 (Techno Festival in NL).
## Functionality of Service
The techno radio service (ThunderWave) is a web app written in Python using Flask and Jinja2. Its features include:
* Listen to radio
* Upload a mp3 file
* Search already accepted proposals
* Write in your profile bio/ festivals you visited
* Read history of Thunderwave Radio Station

# Vulnerabilities
The services has certain vulnerabilities that could be exploited by attackers.
- Vulnerability 1: Read comments of Others MP3 files
- Vulnerability 2: Read Porfile of Others 
## Vulnerability 1: Read comments of Others MP3 files
### Level
Intermediate
### Category
Server Side Template Injection (SSTI) in Jinja2 
### Description
The feature to upload an mp3 file has a vulnerability. Via the `artist` and `title` field of an uploaded mp3 you can inject things into the template. It then gets rendered by jinja2.
The vulnerable code parts:
``` Python
    def set_title_and_artist(self, title, artist, username):
        if artist is None or title is None:
            ...
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
```
The code is from `html_container.py`. In the blocklist somethings are blocked. Nearly every number except of `1` and `6`. It also replaces `+` to `'`. This is included since the html escaping would otherwise escape them (a bit hacky solution).
It is vulnerable since it not escaping SSTI properly and uses in `server.py` jinja2 template string rendering:
``` Python
render_template_string(
        html_con.set_title_and_artist(
            meta_data[1], meta_data[0], current_user.username
        ))
```
### Exploit
1. Create an account. 
2. Create a mp3 file with the following properties:
    `artist` or `title` is set to `'{{[].__class__.__mro__[1].__subclasses__()[-61].get_comments(html_con,+FLAGUSERNAME+)}}'` and genre to `Techno`. Note you need to have some value for either `title` and `artist`.
3. Upload the mp3 file.
4. If it is a valid mp3 file you now can obtain by calling the `get_comments` function of `html_container`.
   The flag is in base64 in the comment field of the `<FLAGUSERNAME>.mp3` file.

How to come up with the exploit? Attackers can Blocklist. Then regonizes that is not blocking everything. Use the `artist` or `title` field to inject a subclasses print. That way they can obtain more information about all subclasses. Since they can only use 1,6,61,66,116,161,166,... -61. They have a bit of a hint. Further if they saw the injection they already got familiar with html_container.py. They can see that there exists an instance of html_container inside server.py which allows them to call funciton out of html_container. Since get_comments is very random it should make them suspicious.

Some assumptions but I am predicting attackers to be curious by trying to attack a service.
### Fix
You need to prevent SSTI. Therefor you can use markup library. 
Then you escape the input/ user controlled variables. Now, a SSTI should be
impossible to successfully execute on the website since input variables get
sanitized.
## Vulnerability 2: Read Profile of Others
### Level
Beginner
### Category
Authentication
### Description
Users can write some infos in their profile and save them. These infos are only visible by them (actually bad design decision. Only occured to me now after writing it down ☹️). They can write a bio and list the festivals they visit.
The function to see your profile looks like that:
``` Python
# User profile page
@app.route("/about_<username>", methods=["GET", "POST"])
@cross_origin()
@login_required
def profile(username):
    if request.method == "GET":
        if current_user.username.lower() != username.lower():
            return "Not authorized", 401
        # load profile
        data = get_profile_from_database(username)
        return render_template_string(
            html_container.profile_html,
            username=current_user.username,
            bio=data[0],
            festivals=data[1],
        )
```
Which is part of the `server.py` file.
As visual there is the authorization check for `GET` requests that looks like `if current_user.username.lower() != username.lower():`. That is vulnerable since "Example", "ExAmple", "example" and "examplE" would all have been accepted by the authorization check. Even though in the server logic they are different users.
That way you can see profiles of others if you have the same name as them just in a different lower and uppercase letter combination.

### Exploit
1. Create an account with the same name as the flag owner. Just not entirely identical.
   E.g., if flag owner accounts name is `ExAmPleName` you as an attack register an account
   with a name that differ at least with one letter upper-/lower case, like `exampleName`.
2. Login in and click on about me in the navbar. This opens your profile page.
3. Change url in urlbar from `/about_exampleName` to `/about_ExAmPleName` and reload page.
4. Know you can see the profile of the flag owner and read the flag from the festivals field.

Demo video:
<video width="320" height="240" controls>
  <source src="../demo_vuln2.mp4" type="video/mp4">
</video>
### Fix
- Remove the `lower() != ... .lower()` in the username check
---
