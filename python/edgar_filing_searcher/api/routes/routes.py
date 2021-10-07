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
    """Search for companies by company name or name of issuer"""
    if "q" in request.args:
        return company_by_company_name(request.args.get("q"))
    if "company_name" in request.args:
        return company_by_company_name(request.args.get("company_name"))
    if "name_of_issuer" in request.args:
        return company_by_invested_company(request)
    return abort(400, description="Bad Request")


def filter_by_date(filings):
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)

    if start_date:
        filings = filings.join(EdgarFiling).filter(
            EdgarFiling.filing_date >= datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
        )

    elif end_date:
        filings = filings.join(EdgarFiling).filter(
            EdgarFiling.filing_date <= datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
        )

    elif start_date and end_date:
        filings = filings.join(EdgarFiling).filter(
            EdgarFiling.filing_date >= datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
        )
    filings = filings.filter(
        EdgarFiling.filing_date <= datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
    )

    return filings


def company_by_company_name(company_name):
    """Search for companies by name of issuer"""
    if company_name is None:
        abort(400, description="Bad Request")

    companies = Company.query.filter(Company.company_name.ilike(f"%{company_name}%"))

    companies_filtered_by_date = filter_by_date(companies)

    return jsonify(list(companies_filtered_by_date))


def company_by_invested_company(request_):
    """Search for companies by invested company"""
    name_of_issuer = request_.args.get('name_of_issuer')
    if name_of_issuer is None:
        abort(400, description="Bad Request")

    companies = Company.query \
        .join(EdgarFiling) \
        .join(Data13f) \
        .filter(Data13f.name_of_issuer.ilike(f"%{name_of_issuer}%"))

    companies_filtered_by_date = filter_by_date(companies)

    return jsonify(list(companies_filtered_by_date))


@company_blueprint.route('/company/<company_id>/edgar-filing/')
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


@company_blueprint.route('/edgar-filing/<filing_id>/data/')
def get_edgarfilings_by_filing_id(filing_id):
    """Route for data for specified edgar filing"""
    data13f = Data13f.query.filter(Data13f.accession_no == filing_id)
    return jsonify(list(data13f))


@company_blueprint.route('/company/<company_id>')
def get_company_by_company_id(company_id):
    """Route company for company_id"""
    company = Company.query.filter(Company.cik_no == company_id).first()
    if company is None:
        return abort(404, description="Not Found")
    return jsonify(company)
