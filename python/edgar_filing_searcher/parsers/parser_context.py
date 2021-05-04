"""Creates a Flask SQLAlchemy app"""
import os
from flask import Flask
from edgar_filing_searcher.database import db


def create_app():
    """This function creates a Flask SQLAlchemy app context to be used for sqlalchemy parser"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app
