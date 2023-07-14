# Service Documentation
Author: Tomer Yavor
## Functionality of Service
The techno radio service (ThunderWave) is a web app written in Python using Flask and Jinja2. Its key features include:

- Feature 1: [Description of feature 1]
- Feature 2: [Description of feature 2]
- Feature 3: [Description of feature 3]

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

### Exploit

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
### Exploit
1. Create an account with the same name as the flag owner. Just not entirely identical.
   E.g., if flag owner accounts name is `ExAmPleName` you as an attack register an account
   with a name that differ at least with one letter upper-/lower case, like `exampleName`.
2. Login in and click on about me in the navbar. This opens your profile page.
3. Change url in urlbar from `/about_exampleName` to `/about_ExAmPleName` and reload page.
4. Know you can see the profile of the flag owner and read the flag from the festivals field.
### Fix
- Remove the `lower() != ... .lower()` in the username check
---
