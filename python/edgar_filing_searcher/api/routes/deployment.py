"""Route for deployment"""
import os

from flask import Blueprint

deployment_blueprint = Blueprint('deployment', __name__)


@deployment_blueprint.route('/update')
def deploy_main():
    """Deploy main"""
    os.system('/home/robo/update_script.sh &>> /home/robo/deploy.log')
    return 'Deployed Main Branch'
