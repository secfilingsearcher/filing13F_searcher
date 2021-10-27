"""API for web back-end"""
import os
from datetime import date

from flask import Blueprint

company_blueprint = Blueprint('company', __name__)


@company_blueprint.route('/update')
def deploy_main():
    """Deploy main"""
    today = date.today()
    today_formatted = today.strftime("%y_%m_%d")
    os.system(f'/home/robo/update_script.sh &>> /home/robo/install_{today_formatted}.log')
    return 'Deployed Main'
