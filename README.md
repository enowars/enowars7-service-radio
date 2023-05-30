# enowars7-service-radio

## Functions
* Listen to radio
* Upload a mp3 file
* Search already accepted proposals



## Vulnerability
* SSTI --> In config is flag, flag can also obtained by creating a user like "ad" and then to go to "/UPLOAD_FOLDER/admin.mp3" since it only checks if username is in file name of the file you want to obtain. Since admin.mp3 contains flag you can read it that way too, it is stored in the comment tag of the audio file
* SQL Injection --> one of the entries in DB contains flag (NOT YET)

## Run service
* docker-compose up --build
* server runs on port 8001
* you need to register and then to login in
* you can listen to radio, uploaded songs and see dummy  db
