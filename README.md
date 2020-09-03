# flaskflick
Python REST API written in flask to save and retrive movies

[Live Demo](https://flaskflick.herokuapp.com/)

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
