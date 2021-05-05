"""APi for web back-end"""
from flask import jsonify, Blueprint, request
from edgar_filing_searcher.models import EdgarFiling

filing_blueprint = Blueprint('edgarfiling', __name__)


@filing_blueprint.route('/edgarfiling/<company_id>')
def get_filings(company_id):
    """Route for results for search by company id"""
    filings = EdgarFiling.query.filter(EdgarFiling.cik_no.like(f"{company_id}%"))
    return jsonify(list(filings))
