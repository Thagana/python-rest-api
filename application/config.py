import os

db_path = os.path.join(os.path.dirname(__file__), 'database.sqlite') 
db_uri = 'sqlite:///{}'.format(db_path)
DEBUG = True
SQLALCHEMY_DATABASE_URI = db_uri
SECRET_KEY = 'b0a149c345bd4660864bac22a677e59a'
SQLALCHEMY_TRACK_MODIFICATIONS = False