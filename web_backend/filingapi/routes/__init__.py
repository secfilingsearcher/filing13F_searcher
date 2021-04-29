"""Filing api init file"""
from filingapi.routes.api import company
from filingapi import create_app

app = create_app()
