import json as json
from flask import Blueprint, render_template, current_app, g, jsonify

from app.shared.request import api_response
from ..shared.Authentification import Auth
from app.models import UserModel, PostModel
from app.models.UserModel import UserSchema

main = Blueprint('main', __name__)


from app.shared.db_api import execute_query

@main.route('/testmain', methods = ['GET'])
@Auth.auth_required
def testmain():
    return api_response({'status': 'App is working !'})


