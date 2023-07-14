# enowars7-service-radio
<img src="Screenshot 2023-07-14 at 14-07-51 Thunderwave Radio.png">

## Functions
* Listen to radio
* Upload a mp3 file
* Search already accepted proposals
* Write in your profile bio/ festivals you visited
* Read history of Thunderwave Radio Station



## Vulnerability
* SSTI (intermiedate)
* Bypass profile control mechanism to obtain flag (beginner)

## Run service
* docker-compose up --build
* server runs on port 8001
* you need to register and then to login in
* you can listen to radio, uploaded songs and see dummy  db


### Via SSTI:
1. Create an account. 
2. Create a mp3 file with the following properties:
    `artist` or `title` is set to `''` and genre to `Techno`. Note you need to have some value for either `title` and `artist`
3. Upload the mp3 file.
4. If it is a valid mp3 file you now can obtain the configs of the app and in the config is a field 
  `FLAG:` where the raw data is written of the `<FLAGUSERNAME>.mp3` file. It should also have the comment tag where the flag lies in plaintext.
### Via path
1. Create an account with the same name as the flagstore account
2. Go to "about me" and change url to match the profile you want to see (e.g. `about_FlagStoreUsername`).
3. The Flag can there be found in the festivals section.


