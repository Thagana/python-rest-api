from flask import request, jsonify, make_response
from application import app, db
from functools import wraps
from .models import User, Movie
import uuid
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def make_admin(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted to Admin!'})

@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/api/v1/movies', methods=['GET'])
@token_required
def get_all_movies(current_user):

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
@token_required
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
@token_required
def add_movie():

    data = request.get_json()

    new_movie = Movie(name=data['name'], description=data['description'],rating=data['rating'], awards_won=data['awards_won'])
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({'massage':'A Movie was added!'})

@app.route('/api/v1/movies/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()

    if not movie:
        return jsonify({'massage':'Not Matching Movie found!'})

    db.session.delete(movie)
    db.session.commit()

    return jsonify({'massage':'movie deleted succesfully'})

@app.route('/api/v1/movies/<movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id)

    if not movie:
        return jsonify({'massage':'No movie found'})
    data = request.get_json()

    update_mov = Movie(name=data['name'], description=data['description'],rating=data['rating'], awards_won=data['awards_won'])
    db.session.add(update_mov)
    db.session.commit()
