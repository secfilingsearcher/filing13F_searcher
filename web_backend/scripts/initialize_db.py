"""Initialize Database"""
from filingapi.database import db
from filingapi import create_app


if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    db.create_all()
