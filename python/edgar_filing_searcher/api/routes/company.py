"""APi for web back-end"""
from datetime import datetime

from flask import jsonify, Blueprint, request
from edgar_filing_searcher.models import Company, EdgarFiling

company_blueprint = Blueprint('company', __name__)

@company_blueprint.after_request
def after_request(response):
    """Enables cross origin resource sharing"""
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response



@company_blueprint.route('/company/search')
def get_company():
    """Route for results for search by company name"""
    company_name = request.args.get('q')
    if company_name:
        companies = Company.query.filter(Company.company_name.ilike(f"%{company_name}%"))
        for company in list(companies):
            cik_no_val = company.cik_no
            cik_edgar_filings = filings(cik_no_val)
            filing_cnt = 0
            for filing in cik_edgar_filings:
                filing_cnt += 1
            companies.filing_cnt = filing_cnt
        return jsonify(list(companies))

    return jsonify([])


@company_blueprint.route('/company/<cik_no>/edgarfiling/')
def get_filings(cik_no):
    """Route for results for search by company id"""
    return jsonify(filings(cik_no))


def filings(cik_no):
    """"""
    date_format = '%Y-%m-%d'
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    filings = EdgarFiling.query.filter(EdgarFiling.cik_no.like(f"{cik_no}%"))

    if start_date:
        filings = filings.filter(
            EdgarFiling.filing_date >= datetime.strptime(start_date, date_format)
        )
    if end_date:
        filings = filings.filter(
            EdgarFiling.filing_date <= datetime.strptime(end_date, date_format)
        )
    return list(filings)
