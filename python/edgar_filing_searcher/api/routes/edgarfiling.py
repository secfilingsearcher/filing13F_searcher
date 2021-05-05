"""APi for web back-end"""
from datetime import datetime
from flask import jsonify, Blueprint, request
from edgar_filing_searcher.models import EdgarFiling

filing_blueprint = Blueprint('edgarfiling', __name__)


@filing_blueprint.route('/edgarfiling/<company_id>')
def get_filings(company_id):
    """Route for results for search by company id"""
    date_format = '%Y-%m-%d'
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    filings = EdgarFiling.query.filter(
        EdgarFiling.cik_no.like(f"{company_id}%"),
        EdgarFiling.filing_date >= datetime.strptime(start_date, date_format),
        EdgarFiling.filing_date <= datetime.strptime(end_date, date_format)
    )

    return jsonify(list(filings))
