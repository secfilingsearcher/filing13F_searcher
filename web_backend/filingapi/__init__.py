"""Flask app initializing code."""
import os
from flask import Flask
from web_backend.filingapi.database import db


def create_app():
    """Create Flask app and create database."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
    db.init_app(app)

    # pylint: disable=import-outside-toplevel
    from web_backend.filingapi.routes import company
    app.register_blueprint(company)
    return app


