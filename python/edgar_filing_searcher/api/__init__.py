"""Flask app initializing code."""
import os
from flask import Flask
from edgar_filing_searcher.api.database import db
from edgar_filing_searcher.api.routes.company import company_blueprint


def create_app():
    """Create Flask app and create database."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
    db.init_app(app)
    app.register_blueprint(company_blueprint)
    return app