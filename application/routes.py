from flask import request, jsonify, make_response
from application import app, db, jwt
from functools import wraps
from .models import User, Movie
import uuid
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


@app.route('/login', methods=['POST', 'GET'])
def login():
    data = request.get_json()

    # Check if there is data sent
    if not data['username']:
        return jsonify({'error': 'Username not set'}), 400
    if not data['password']:
        return jsonify({'error': 'Password not set'}), 400

    user = User.query.filter_by(name=data['username']).first()

    if user is None:
        return jsonify({'error': 'Could not find user'})

    if check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=data['username'])
        return jsonify(access_token=access_token), 200

    return jsonify({'error': 'Something happend'}), 400


@ app.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User.query.filter_by(name=data['username']).first()
    if user:
        return jsonify({'error': 'User already exists'}), 200
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()),
                    name=data['username'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'}), 201


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@ app.route('/api/v1/movies', methods=['GET'])
@ jwt_required
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


@app.route('/api/v1/movies/<movie_id>', methods=['GET'])
@jwt_required
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


@app.route('/api/v1/movies', methods=['POST'])
@jwt_required
def add_movie():

    data = request.get_json()

    new_movie = Movie(name=data['name'], description=data['description'],
                      rating=data['rating'], awards_won=data['awards_won'])
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({'massage': 'A Movie was added!'})


@app.route('/api/v1/movies/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()

    if not movie:
        return jsonify({'massage': 'Not Matching Movie found!'})

    db.session.delete(movie)
    db.session.commit()

    return jsonify({'massage': 'movie deleted succesfully'})


@app.route('/api/v1/movies/<movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id)

    if not movie:
        return jsonify({'massage': 'No movie found'})
    data = request.get_json()

    update_mov = Movie(name=data['name'], description=data['description'],
                       rating=data['rating'], awards_won=data['awards_won'])
    db.session.add(update_mov)
    db.session.commit()
