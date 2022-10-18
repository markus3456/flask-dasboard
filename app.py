from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/finance'  #connect to database on localhost
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
             #define variable to use modules of SQLAlchemy in this app

    return app