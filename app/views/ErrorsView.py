from flask import Blueprint, render_template, current_app

from app.shared.request import api_response


errors = Blueprint('errors', __name__)


#custome error handler
@errors.app_errorhandler(404)
def page_not_found(error):
    return api_response({'error': 'No data found'}, 404)

@errors.app_errorhandler(500)
def server_error(error):
    return api_response({'error': 'Something went wrong'}, 500)