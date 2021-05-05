"""APi for web back-end"""
from flask import jsonify, Blueprint, request
from edgar_filing_searcher.models import Company

company_blueprint = Blueprint('company', __name__)


@company_blueprint.route('/company/search')
def get_company():
    """Route for results for search by company name"""
    company_name = request.args.get('q')
    if company_name:
        companies = Company.query.filter(Company.company_name.ilike(f"%{company_name}%"))
        return jsonify(list(companies))
    else:
        return jsonify([])