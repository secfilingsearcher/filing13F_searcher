from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'DB_CONNECTION_STRING'

db = SQLAlchemy(app)

@app.route('/<company_id>')
def get_company(id):
    pass


@app.route('/<company_id>/filings')
def get_filings(id):
    pass


@app.route('filings/<filing_id>')
def get_filing(id):
    pass




