from flask import Flask, jsonify, Blueprint
from web_backend.filingapi.models import PrimaryDoc

company = Blueprint('company', __name__)

@company.route('/')
def index():
    primary_docs = PrimaryDoc.query.all()
    return jsonify(primary_docs)


@company.route('/company/<company_id>')
def get_company(company_id):
    primary_doc = PrimaryDoc.query.filter(PrimaryDoc.company_name.like(f"{company_id}%"))
    return jsonify(list(primary_doc))


@company.route('/company/<company_id>/filings')
def get_filings(id):
    pass


@company.route('/filings/<filing_id>')
def get_filing(id):
    pass




