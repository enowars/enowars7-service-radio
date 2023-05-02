# enowars7-service-radio

* MP3 player 
* C++ / Rust/ Python 
* Player only checks header and SQL Code inject since DB model is stupid and saves parts of mp3 to read meta data
* QUIC downgrade to HTTP/1 plaintext (UDP throttling)

## Where to store flag? 
* DB ensure that can’t drop or delete flags (permission check)
* Real mp3 snippet which stores mp3 decode and encode flag into mp3 (spells flag)
* Make slightly different behavior for HTTP 
* Race condition error 
