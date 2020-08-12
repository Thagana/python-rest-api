from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
app = Flask(__name__)
app.config.from_pyfile('config.py')
jwt = JWTManager(app)
db = SQLAlchemy(app)



from application import routes