"""Filing api init file"""
from filingapi.routes.company import company_blueprint
from filingapi import create_app

app = create_app()
