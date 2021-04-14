from flask import Flask
from database import db_session, init_db


app = Flask(__name__)


@app.before_first_request
def setup_db():
    init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/company/<company_id>')
def get_company(id):
    pass


@app.route('/company/<company_id>/filings')
def get_filings(id):
    pass


@app.route('/filings/<filing_id>')
def get_filing(id):
    pass




