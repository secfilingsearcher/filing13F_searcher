"""APi for web back-end"""
from datetime import datetime

from flask import jsonify, Blueprint, request, abort

from edgar_filing_searcher.models import Company, EdgarFiling, Data13f

company_blueprint = Blueprint('company', __name__)


@company_blueprint.after_request
def after_request(response):
    """Enables cross origin resource sharing"""
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


@company_blueprint.route('/company/search')
def search_company():
    """Search for companies by company name"""
    company_name = request.args.get('q')
    companies = Company.query.filter(Company.company_name.ilike(f"%{company_name}%"))

    if company_name is None:
        abort(400, description="Bad Request")

    return jsonify(list(companies))


@company_blueprint.route('/company/<company_id>/edgarfiling/')
def get_edgarfilings_with_date(company_id):
    """Route for filings for the specified company, optionally filtered by date"""
    date_format = '%Y-%m-%d'
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    filings = EdgarFiling.query.filter(EdgarFiling.cik_no == company_id)

    if start_date:
        filings = filings.filter(
            EdgarFiling.filing_date >= datetime.strptime(start_date, date_format)
        )
    if end_date:
        filings = filings.filter(
            EdgarFiling.filing_date <= datetime.strptime(end_date, date_format)
        )

    return jsonify(list(filings))


@company_blueprint.route('/edgarfiling/<accession_no>/data/')
def get_edgarfilings_by_accession_no(accession_no):
    """Route for data for specified edgar filing"""
    data13f = Data13f.query.filter(Data13f.accession_no == accession_no)
    return jsonify(list(data13f))
