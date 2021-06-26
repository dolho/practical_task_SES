import hashlib
import os
import pathlib
import json
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from . import token
from app.blueprints.user.email_worker import send_confirmation_email
from flask import url_for
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

SECRET_SALT = os.environ['SECRET_SALT']


def get_number_of_file(email):
    return int(hashlib.sha256(email.encode('utf-8')).hexdigest(), 16) % (5 * 10 ** 6)


def create_user(email: str, password: str, host: str = '') -> bool:
    number_of_file = get_number_of_file(email)
    path_to_file = os.path.join(pathlib.Path(__file__).parent.absolute(),
                                "user_data", str(number_of_file) + '.json')
    is_file_already_exists = os.path.isfile(path_to_file)
    if is_file_already_exists:
        with open(path_to_file, 'r+') as f:
            data = json.load(f)
            for i in data:
                if i['email'] == email:
                    raise ValueError

            user_dict = {'email': email, 'password_hash': generate_password_hash(password), 'is_activated': False}
            data.append(user_dict)
            # It is needed to overwrite file
            f.seek(0)
            f.truncate()
            json.dump(data, f)
    else:
        user_dict = {'email': email, 'password_hash': generate_password_hash(password), 'is_activated': False}
        with open(path_to_file, 'w') as f:
            list_of_dicts = list()
            list_of_dicts.append(user_dict)
            json.dump(list_of_dicts, f)
            # f.write(json.dumps(list_of_dicts))
    user_token = token.generate_confirmation_token(email)
    activation_url = host + url_for('user.confirm_email', token=user_token)
    # print(email, type(email), user_token, type(user_token))
    result = send_confirmation_email.delay(email, activation_url)
    return True


def login_user(email:str, password: str) -> bool:
    number_of_file = get_number_of_file(email)
    path_to_file = os.path.join(pathlib.Path(__file__).parent.absolute(),
                                "user_data", str(number_of_file) + '.json')
    is_file_already_exists = os.path.isfile(path_to_file)
    if is_file_already_exists:
        with open(path_to_file, 'r+') as f:
            data = json.load(f)
            for i in data:
                if i['email'] == email:
                    res = check_password_hash(i['password_hash'], password)
                    if not res:
                        raise ValueError
                    token_expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                    encoded_jwt = jwt.encode({"email": email, "is_activated": i['is_activated'],
                                              'exp': token_expires}, SECRET_SALT, algorithm="HS256")
                    return encoded_jwt
    else:
        raise FileNotFoundError


def activate_account(email:str):
    number_of_file = get_number_of_file(email)
    path_to_file = os.path.join(pathlib.Path(__file__).parent.absolute(),
                                "user_data", str(number_of_file) + '.json')
    is_file_already_exists = os.path.isfile(path_to_file)
    if is_file_already_exists:
        with open(path_to_file, 'r+') as f:
            data = json.load(f)
            for i in data:
                if i['email'] == email:
                    i['is_activated'] = True
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f)
    else:
        raise FileNotFoundError


def delete_user(email):
    number_of_file = get_number_of_file(email)
    path_to_file = os.path.join(pathlib.Path(__file__).parent.absolute(),
                                "user_data", str(number_of_file) + '.json')
    is_file_already_exists = os.path.isfile(path_to_file)
    if is_file_already_exists:
        with open(path_to_file, 'r+') as f:
            data = json.load(f)
            for i in data:
                if i['email'] == email:
                    data.remove(i)
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f)
                    break
