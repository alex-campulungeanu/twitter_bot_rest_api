import re

from flask import Blueprint, current_app, request, g
from flask_security.views import forgot_password

from app.constants.regexp_list import *
from app.models import db
from app.models.UserModel import UserModel
from app.models.RoleModel import RoleModel
from app.models.UserTokenModel import UserTokenModel
from app.shared.helper import validate_password
from app.shared.request import api_response
from app.shared.email import send_password_reset_email
from app.shared.Authentification import Auth
from app.shared.request import validate_request
from app.constants import app_constants

user_api = Blueprint('user_api', __name__)

@user_api.route('/signup', methods=['POST'])
@validate_request('email', 'name', 'password', 'secret_word')
def signup():
    req_data = request.get_json()
    res = {'status': '', 'data': {}, 'error': {}}
    email = req_data['email']
    name = req_data['name']
    password = req_data['password']
    secret_word = req_data['secret_word']
    if not re.match(email_regexp, email):
        res['status'] = app_constants.notok_status
        res['error'] = 'Email pattern not ok !'
        return api_response(res, 400)
    elif validate_password(password) != True: #poate ar trebui sa scriu altfel asta :)
        res['status'] = app_constants.notok_status
        res['error'] = validate_password(password)
        return api_response(res, 400)
    elif secret_word != current_app.config['SECRET_WORD_REGISTRATION']:
        res['status'] = app_constants.notok_status
        res['error'] = 'Wrong secret word !'
        return api_response(res, 400)
    else:
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            new_user = UserModel(name=name, email=email, password=password)
            role = RoleModel.query.get(app_constants.ROLE_USER)
            new_user.roles.append(role)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            res['status'] = app_constants.ok_status
            return api_response(res)
        else:
            res['status'] = app_constants.notok_status
            res['error'] = 'User already exist !'
            return api_response(res, 400)

@user_api.route('/login', methods=['POST'])
@validate_request('email', 'password')
def login():
    req_data = request.get_json()
    res = {'status': app_constants.ok_status, 'data': {}, 'error': {}}
    email = req_data['email']
    password = req_data['password']
    user = UserModel.query.filter_by(email=email).first()
    if user and user.check_password(password):
        jwt_token = Auth.generate_token(user.id)
        res['status'] = app_constants.ok_status
        res['data'] = {'token': jwt_token}
        if current_app.config['JWT_CHECK_DB']:
            user_token = UserTokenModel(token=jwt_token, user_id = user.id)
            db.session.add(user_token)
            db.session.commit()
        return api_response(res, 200)
    else:
        res['status'] = app_constants.notok_status
        res['error'] = 'User or password is incorrect'
        return api_response(res, 401)
    
@user_api.route('/forgot_password_request', methods=['POST'])
@validate_request('email')
def forgot_password_request():
    req_data = request.get_json()
    res = {'status': '', 'data': {}, 'error': {}}
    email = req_data['email']
    user = UserModel.query.filter_by(email=email).first()
    if user:
        current_app.logger.info('send email password')
        send_password_reset_email(user)
        res['status'] = app_constants.ok_status
        return api_response(res, 200)
    else:
        res['status'] = app_constants.notok_status
        res['error'] = "User {0} not found in database !".format(email)
        return api_response(res, 401)

@user_api.route('/forgot_password_process/<p_token>', methods=['POST'])
@validate_request('password')
def forgot_password_process(p_token):
    res = {'status': app_constants.ok_status, 'data': {}, 'error': {}}
    req_data = request.get_json()
    new_password = req_data['password']
    user = UserModel.verify_reset_password(p_token)
    if not user:
        res['status'] = app_constants.notok_status
        res['error'] = 'Token is incorrect !'
        return api_response(res, 401)
    user.set_password(new_password)
    db.session.commit()
    res['status'] = app_constants.ok_status
    return api_response(res, 200)

@user_api.route('/change_password', methods=['POST'])
@Auth.auth_required
@validate_request('old_password', 'new_password')
def change_password():
    res = {'status': app_constants.ok_status, 'data': {}, 'error': {}}
    req_data = request.get_json()
    old_password = req_data['old_password']
    new_password = req_data['new_password']
    current_user = g.user
    if not current_user.check_password(old_password):
        res['status'] = app_constants.notok_status
        res['error'] = 'Old password is not ok !'
        return api_response(res, 401)
    elif validate_password(new_password) != True:
        res['status'] = app_constants.notok_status
        res['error'] = validate_password(new_password)
        return api_response(res, 401)
    else:
        user = current_user
        user.set_password(new_password)
        db.session.add(user)
        db.session.commit()
        res['status'] = app_constants.ok_status
        res['data'] = 'Password changed !'
        return api_response(res, 200)
    