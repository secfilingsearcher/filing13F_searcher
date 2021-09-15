"""Flask app initializing code."""
import os

from flask import Flask

from edgar_filing_searcher.api.routes.check_connection_string import postgres_test
from edgar_filing_searcher.api.routes.company import company_blueprint
from edgar_filing_searcher.database import db


def create_app(configuration_file_obj=None):
    """Create Flask app and create database."""
    app = Flask(__name__)
    postgres_test()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if configuration_file_obj:
        app.config.from_object(configuration_file_obj)
    db.init_app(app)
    app.register_blueprint(company_blueprint)
    return app
