"""Flask app initializing code."""
import os
from flask import Flask
from edgar_filing_searcher.database import db
from edgar_filing_searcher.api.routes.company import company_blueprint


def create_app(obj=None):
    """Create Flask app and create database."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if obj:
        app.config.from_object(obj)
    db.init_app(app)
    app.register_blueprint(company_blueprint)
    return app
