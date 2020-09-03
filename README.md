# python-rest-api
Rest api using python flask, sqlite3 and jwt
## First Steps
* create a user
* login
* include x-access-token everywhere needed

> Note! I have already create an admin create a user make him/her/X admin delete user admin then you are go to go

>Note! if you are using vs code you can install rest-client and open restclient.http test using those endpoints...this is very easy


## Movies End Points
### ```GET ALL MOVIES```
```bash
    $ curl http://localhost:5000
```
(auth required)

### ```GET MOVIE ID 1```
```bash
    $ curl http://localhost:5000/api/v1/movies/1
```
(auth required)

### ```DELETE MOVIE ID 1```
```bash
    $ http://localhost:5000/api/v1/movies/1
```
(auth required)

### ```PUT UPDATE MOVIE ID 1```
```bash
    $ curl http://localhost:5000/api/v1/movies/1
```
(auth required)
