"""APi for web back-end"""
from flask import jsonify, Blueprint
from filingapi.models import Company

company_blueprint = Blueprint('company', __name__)


@company_blueprint.route('/company/<company_id>')
def get_company(company_id):
    """Route for results for search by company id"""
    companies = Company.query.filter(Company.cik_no.like(f"{company_id}%"))
    return jsonify(list(companies))

#
# @company_blueprint.route('/company/<company_id>/filings')
# def get_filings(company_id):
#     """Route for results for retrieval of filings"""
#     filings = Infotable.query.filter(Infotable.cik_no == company_id)
#     return jsonify(list(filings))
#
#
# @company_blueprint.route('/filings/<filing_id>')
# def get_filing(filing_id):
#     """Route for result of search for specific filing by filing_id"""
#     filing = Infotable.query.filter(Infotable.row_id == filing_id).first()
#     return jsonify(filing)
