from base64 import b64encode
import hashlib
import json
import os

from werkzeug.utils import secure_filename
from flask import current_app, request, Blueprint, jsonify, g
from sqlalchemy.exc import IntegrityError

from app.shared.helper import is_allowed_for_post, image2base64, generate_random_string, string2md5, generate_unique_string
from app.shared.request import api_response, validate_request
from app.models.PostModel import PostModel#, PostSchema
from app.models.UserModel import UserModel, UserSchema
from app.models.PlatformModel import PlatformModel
from app.models import db, cfg_db_schema
from app.shared.db_api import execute_query
from app.constants import app_constants, stop_words_list
from app.shared.Authentification import Auth
from app.utils.apis.chuck_norris_facts import get_chuck_norris_facts

post_api = Blueprint('post_api', __name__)


@post_api.route('/upload_post_files', methods=['POST'])
@Auth.auth_required
@Auth.check_permissions('createPost')
def upload_post_files():
    res = {'status': '', 'data': {}, 'error': {}}
    files = request.files.getlist('files[]')
    if len(files) == 0:
        res['status'] = 'notok'
        res['error'] = 'No files selected'
        return api_response(res)
    valid_files = []
    invalid_files = []
    for file in files:
        file_read = file.read() #!!! i need to store de read value into a variable because the cursor moves to end after every read
        if is_allowed_for_post(file.filename):
            filename = secure_filename(file.filename) + '_' + generate_random_string()
            md5 = hashlib.md5(file_read).hexdigest()
            files_existing = PostModel.query.filter_by(md5=md5).all()
            if len(files_existing) == 0:
                image_str = str(image2base64(file_read))
                new_post = PostModel(name=filename, body=image_str, md5=md5, post_type_id=app_constants.POST_TYPE_IMAGE, user_id = g.user.id)
                db.session.add(new_post)
                db.session.commit()
                valid_files.append({'name':file.filename, 'error': ''})
            else: 
                invalid_files.append({'name':file.filename, 'error': 'File already exist'})
        else:
            invalid_files.append({'name':file.filename, 'error': 'Wrong format'})
    # current_app.logger.info(f'Fisierele valide sunt: {valid_files}')
    # current_app.logger.info(f'Fisierele invalide sunt: {invalid_files}')
    return api_response(valid_files + invalid_files)

@post_api.route('/upload_post_text', methods=['POST'])
@Auth.auth_required
@Auth.check_permissions('createPost')
@validate_request('source_type', 'nr_of_calls')
def upload_post_text():
    res = {'status': '', 'data': {}, 'error': {}}
    req_data = request.get_json()
    source_type = req_data['source_type']
    nr_of_calls = req_data['nr_of_calls']
    post_list = [] 
    post_list_success = []
    post_list_failed = []
    ## source type must be: api or json file
    if source_type == 'chuck_norris':
        for i in range(nr_of_calls):
            chuk_joke = get_chuck_norris_facts() ## call chuck norris api
            chuck_url = chuk_joke['url']
            chuck_body = chuk_joke['value']
            post_list.append({'name': chuck_url, 'body': chuck_body, 'error:': ''})
    elif os.path.splitext(source_type)[1] == '.json': ## file should be .json type in utils/jokes ...
        file_path = current_app.root_path + '/utils/joke_files/' + source_type
        with open(file_path) as file:
            data = json.load(file)
            for line in data:
                name = source_type + '-' + str(line['name'])
                body = line['body']
                post_list.append({'name': name, 'body': body, 'error:': ''})
    else:
        res['status'] = 'notok'
        res['error'] = 'Incorrect post source'
        return api_response(res)
    ## add list of posts to DB
    for post in post_list:
        md5 = string2md5(post['body'])
        new_post = PostModel(name = post['name'], body=post['body'], md5=md5, post_type_id=app_constants.POST_TYPE_TEXT, user_id=g.user.id)
        try:
            db.session.add(new_post)
            db.session.commit()
            post_list_success.append(post)
        except IntegrityError as unique:
            db.session.rollback() 
            post.update({'error:': 'Post already added in DB'})
            post_list_failed.append(post)
    res['status'] = 'ok'
    res['data'] = {'success': post_list_success, 'failed': post_list_failed}
    return api_response(res)

@post_api.route('/upload_manual_post_text', methods=['POST'])
@Auth.auth_required
@Auth.check_permissions('createPost')
@validate_request('name', 'body')
def upload_manual_post_text():
    res = {'status': '', 'data': {}, 'error': {}}
    req_data = request.get_json()
    name = generate_unique_string(req_data['name'])
    body = req_data['body']
    md5 = string2md5(body)
    if len(req_data['name']) > 50: 
        return api_response({'status': 'notok', 'error:': 'Name is longer than 50 chars'})
    new_post = PostModel(name=name, body=body, md5=md5, post_type_id=app_constants.POST_TYPE_TEXT, user_id=g.user.id)
    try:
        db.session.add(new_post)
        db.session.commit()
    except IntegrityError as unique:
        db.session.rollback() 
        return api_response({'status': 'notok', 'error:': 'Post already added in DB'})
    res['status'] = 'ok'
    res['data'] = 'Post added to DB'
    return api_response(res)