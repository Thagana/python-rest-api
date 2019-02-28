# python-rest-api
Rest api using python flask, sqlite3 and jwt
## First Steps
* create a user
* login
* include x-access-token everywhere needed

> Note! I have already create an admin create a user make him/her/X admin delete user admin then you are go to go

>Note! if you are using vs code you can install rest-client and open restclient.http test using those endpoints...this is very easy

##Users End Points
### GET ALL USERS
https://localhost:5000/user
(auth required)

### GET ONE USER ID 1
http://localhost:5000/user/1
(auth required)

### DELETE USER ID 1
http://localhost:5000/user/1
(auth required)

### PUT UDATE USER ID 1
http://localhost:5000/user/1
(auth required)

### POST CREATE A USER
http://localhost:5000/user
(auth required)

## Movies End Points
### GET ALL MOVIES
http://localhost:5000/api/v1/movies
(auth required)

### GET MOVIE ID 1
http://localhost:5000/api/v1/movies/1
(auth required)

### DELETE MOVIE ID 1
http://localhost:5000/api/v1/movies/1
(auth required)

### PUT UPDATE MOVIE ID 1
http://localhost:5000/api/v1/movies/1
(auth required)
