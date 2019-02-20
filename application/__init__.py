from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretekey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\SAMUEL\\Documents\\Programming\\others\\Path\\src\API\\flask_apii\\book-api\\book.db'

db = SQLAlchemy(app)



from application import routes