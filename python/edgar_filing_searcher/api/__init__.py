"""Flask app initializing code."""
import os

from flask import Flask

from edgar_filing_searcher.api.utils import check_connection_string
from edgar_filing_searcher.api.routes.filing13f import filing13f_blueprint
from edgar_filing_searcher.api.routes.deployment import deployment_blueprint
from edgar_filing_searcher.database import db


def create_app(configuration_file_obj=None):
    """Create Flask app and create database."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if configuration_file_obj:
        app.config.from_object(configuration_file_obj)
    check_connection_string(app.config['SQLALCHEMY_DATABASE_URI'])
    db.init_app(app)
    app.register_blueprint(filing13f_blueprint)
    app.register_blueprint(deployment_blueprint)
    return app
