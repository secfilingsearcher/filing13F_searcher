"""APi for web back-end"""
from datetime import datetime

from flask import jsonify, Blueprint, request

from edgar_filing_searcher.models import Company, EdgarFiling, Data13f

company_blueprint = Blueprint('company', __name__)


@company_blueprint.after_request
def after_request(response):
    """Enables cross origin resource sharing"""
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


@company_blueprint.route('/company/search')
def get_company():
    """Route for search results by company name"""
    company_name = request.args.get('q')
    if company_name:
        companies = Company.query.filter(Company.company_name.ilike(f"%{company_name}%"))
        return jsonify(list(companies))

    return jsonify([])


@company_blueprint.route('/company/<company_id>/edgarfiling/')
def get_filings(company_id):
    """Route for search results of filings by company id and date"""
    date_format = '%Y-%m-%d'
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    filings = EdgarFiling.query.filter(EdgarFiling.cik_no.like(f"{company_id}%"))

    if start_date:
        filings = filings.filter(
            EdgarFiling.filing_date >= datetime.strptime(start_date, date_format)
        )
    if end_date:
        filings = filings.filter(
            EdgarFiling.filing_date <= datetime.strptime(end_date, date_format)
        )

    return jsonify(list(filings))


@company_blueprint.route('/company/<company_id>/')
def get_filings_from_company(company_id):
    """Route for search results of company by company id"""
    filings = EdgarFiling.query.filter(EdgarFiling.cik_no == company_id)
    return jsonify(list(filings))


@company_blueprint.route('/company/<company_id>/filing/<filing_id>')
def get_filings_from_company_(company_id, filing_id):
    """Route for search results of filing by filing id"""
    data13f = Data13f.query. \
        filter(Data13f.cik_no == company_id, Data13f.accession_no == filing_id)
    return jsonify(list(data13f))
