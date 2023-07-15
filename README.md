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


## Infrastructure
* nginx (Port 5555) in front of gunicorn (gevent)
* flask application (Web app)
* automatic clean up, deleting all files that are older than 30 minutes
