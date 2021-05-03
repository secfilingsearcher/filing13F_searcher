"""APi for web back-end"""
from flask import jsonify, Blueprint
from filingapi.models import Company

company_blueprint = Blueprint('company', __name__)


@company_blueprint.route('/company/<company_id>')
def get_company(company_id):
    """Route for results for search by company id"""
    companies = Company.query.filter(Company.cik_no.like(f"{company_id}%"))
    return jsonify(list(companies))
