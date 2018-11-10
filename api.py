from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretekey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\SAMUEL\\Documents\\Programming\\others\\Path\\src\API\\flask_apii\\book-api\\book.db'

db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    awards_won = db.Column(db.Integer)


@app.route('/api/v1/movies', methods=['GET'])
def get_all_movies():
    movies = Movie.query.all()

    if not movies:
        return jsonify({'massage': 'movie not found!'})    
    output = []

    for movie in movies:
        movie_data = {}
        movie_data['id'] = movie.id
        movie_data['name'] = movie.name
        movie_data['description'] = movie.description
        movie_data['rating'] = movie.rating
        movie_data['awards_won'] = movie.awards_won
   
        output.append(movie_data)

    return jsonify({'movies': output})

@app.route('/api/v1/movie/<movie_id>', methods=['GET'])
def get_one_movie(movie_id):

    movie = Movie.query.filter_by(id=movie_id).first()

    if not movie:
        return jsonify({'massage': 'No movie found!'})

    movie_data = {}
    movie_data['id'] = movie.id
    movie_data['name'] = movie.name
    movie_data['description'] = movie.description
    movie_data['rating'] = movie.rating
    movie_data['awards_won'] = movie.awards_won


    return jsonify(movie_data)

@app.route('/api/v1/movie', methods=['POST'])
def add_movie():

    data = request.get_json()

    new_movie = Movie(name=data['name'], description=data['description'],rating=data['rating'], awards_won=data['awards_won'])
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({'massage':'A Movie was added!'})

@app.route('/api/v1/movie/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()

    if not movie:
        return jsonify({'massage':'Not Matching Movie found!'})

    db.session.delete(movie)
    db.session.commit()

    return jsonify({'massage':'movie deleted succesfully'})

@app.route('/api/v1/movie/<movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id)

    if not movie:
        return jsonify({'massage':'No movie found'})
    data = request.get_json()

    update_mov = Movie(name=data['name'], description=data['description'],rating=data['rating'], awards_won=data['awards_won'])
    db.session.add(update_mov)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)