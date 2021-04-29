"""APi for web back-end"""
from flask import jsonify, Blueprint
from filingapi.models import PrimaryDoc, Infotable

company = Blueprint('company', __name__)


@company.route('/')
def index():
    """Route for index page"""
    primary_docs = PrimaryDoc.query.all()
    return jsonify(primary_docs)


@company.route('/company/<company_id>')
def get_company(company_id):
    """Route for results for search by company id"""
    primary_doc = PrimaryDoc.query.filter(PrimaryDoc.cik_no.like(f"{company_id}%"))
    return jsonify(list(primary_doc))


@company.route('/company/<company_id>/filings')
def get_filings(company_id):
    """Route for results for retrieval of filings"""
    filings = Infotable.query.filter(Infotable.cik_no == company_id)
    return jsonify(list(filings))


@company.route('/filings/<filing_id>')
def get_filing(filing_id):
    """Route for result of search for specific filing by filing_id"""
    filing = Infotable.query.filter(Infotable.row_id == filing_id).first()
    return jsonify(filing)
