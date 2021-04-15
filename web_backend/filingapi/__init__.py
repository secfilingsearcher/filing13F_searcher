import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
    db.init_app(app)

    from web_backend.filingapi.routes import company
    app.register_blueprint(company)
    return app


db = SQLAlchemy()
