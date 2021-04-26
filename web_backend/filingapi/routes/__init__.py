"""Filing api init file"""
from web_backend.filingapi.routes.api import company
from web_backend.filingapi import create_app

app = create_app()
