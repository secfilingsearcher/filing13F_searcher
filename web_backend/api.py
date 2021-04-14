from flask import Flask, jsonify
from database import db_session, init_db
from models import PrimaryDoc, Infotable


app = Flask(__name__)


@app.before_first_request
def setup_db():
    init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def index():
    primary_docs = PrimaryDoc.query.all()
    return jsonify(primary_docs)


@app.route('/company/<company_id>')
def get_company(company_id):
    primary_doc = PrimaryDoc.query.filter(PrimaryDoc.company_name.like(f"{company_id}%"))
    return jsonify(list(primary_doc))


@app.route('/company/<company_id>/filings')
def get_filings(id):
    pass


@app.route('/filings/<filing_id>')
def get_filing(id):
    pass




