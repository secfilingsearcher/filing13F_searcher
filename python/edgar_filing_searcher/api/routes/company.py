"""APi for web back-end"""
from datetime import datetime

from flask import jsonify, Blueprint, request
from edgar_filing_searcher.models import Company, EdgarFiling

company_blueprint = Blueprint('company', __name__)


@company_blueprint.route('/company/search')
def get_company():
    """Route for results for search by company name"""
    company_name = request.args.get('q')
    if company_name:
        companies = Company.query.filter(Company.company_name.ilike(f"%{company_name}%"))
        return jsonify(list(companies))

    return jsonify([])


@company_blueprint.route('/company/<company_id>/edgarfiling/')
def get_filings(company_id):
    """Route for results for search by company id"""
    date_format = '%Y-%m-%d'
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    filings = EdgarFiling.query.filter(EdgarFiling.cik_no.like(f"{company_id}%"))

    if start_date:
        filings = filings.filter(EdgarFiling.filing_date >= datetime.strptime(start_date, date_format))
    if end_date:
        filings = filings.filter(EdgarFiling.filing_date <= datetime.strptime(end_date, date_format))

    return jsonify(list(filings))
