# enowars7-service-radio

## Functions
* Listen to radio
* Upload a mp3 file
* Search already accepted proposals
* Write in your profile bio/ festivals you visited
* Read history of Thunderwave Radio Station



## Vulnerability
* SSTI --> In config is flag, flag can also obtained by creating a user like "ad" and then to go to "/UPLOAD_FOLDER/admin.mp3" since it only checks if username is in file name of the file you want to obtain. Since admin.mp3 contains flag you can read it that way too, it is stored in the comment tag of the audio file (intermiedate)
* Bypass profile control mechanism to obtain flag (beginner)

## Run service
* docker-compose up --build
* server runs on port 8001
* you need to register and then to login in
* you can listen to radio, uploaded songs and see dummy  db

## How to exploit it
Since currently only one exploit works here are the two ways described that I am aware of:

### Via SSTI:
1. Create an account. 
2. Create a mp3 file with the following properties:
    `artist` or `title` is set to `''` and genre to `Techno`. Note you need to have some value for either `title` and `artist`
3. Upload the mp3 file.
4. If it is a valid mp3 file you now can obtain the configs of the app and in the config is a field 
  `FLAG:` where the raw data is written of the `admin.mp3` file. It should also have the comment tag where the flag lies in plaintext.
  Somehow the checker doesn't set it yet.
### Via path
1. Create an account with the same name as the flagstore account
2. Go to "about me" and change url to match the profile you want to see (e.g. `about_FlagStoreUsername`).
3. The Flag can there be found in the festivals section.


