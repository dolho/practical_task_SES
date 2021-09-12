import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from email_confirmation_token import *
# from .file_worker import FileWorker
from email_worker import send_confirmation_email
from flask import url_for
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

SECRET_SALT = os.environ['SECRET_SALT']


# file_worker = file_worker.FileWorker()

class UserModel:

    def __init__(self, file_worker):
        self.__file_worker = file_worker

    def get_number_of_file(self, email):
        return int(hashlib.sha256(email.encode('utf-8')).hexdigest(), 16) % (5 * 10 ** 6)

    @staticmethod
    def create_response(status, message):
        return {"status": status, "message": message}


    def create_user_dict(self, email, password, is_activated=False):
        return {'email': email, 'password_hash': generate_password_hash(password), 'is_activated': is_activated}


    def create_user(self, email: str, password: str, email_confirmation_url: str = '') :
        number_of_file = self.get_number_of_file(email)
        path_to_file = self.__file_worker.get_path_to_file(str(number_of_file))
        try:
            data = self.__file_worker.read_file(path_to_file)
            for i in data:
                if i['email'] == email:
                    raise ValueError
            self.__file_worker.append_to_file(path_to_file, self.create_user_dict(email, password))
        except FileNotFoundError:
            list_of_dicts = list()
            list_of_dicts.append(self.create_user_dict(email, password))
            self.__file_worker.create_file(path_to_file, list_of_dicts)
        user_token = generate_confirmation_token(email)
        print(email_confirmation_url, user_token, email_confirmation_url + user_token)
        result = send_confirmation_email.delay(email, email_confirmation_url + user_token)
        return UserModel.create_response(200, "Ok")


    def login_user(self, email:str, password: str):
        number_of_file = self.get_number_of_file(email)
        path_to_file = self.__file_worker.get_path_to_file(str(number_of_file))
        data = self.__file_worker.read_file(path_to_file)
        for i in data:
            if i['email'] == email:
                res = check_password_hash(i['password_hash'], password)
                if not res:
                    raise ValueError
                token_expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                encoded_jwt = jwt.encode({"email": email, "is_activated": i['is_activated'],
                                          'exp': token_expires}, SECRET_SALT, algorithm="HS256")
                return UserModel.create_response(200, encoded_jwt)
        return UserModel.create_response(404, "No user with such email")

    def activate_account(self, token):
        try:
            email = confirm_token(token)
        except:
            # TODO Разбить except на несколько
            return UserModel.create_response(401, 'Your confirmation link expired')
        number_of_file = self.get_number_of_file(email)
        path_to_file = self.__file_worker.get_path_to_file(str(number_of_file))
        data = self.__file_worker.read_file(path_to_file)
        for i in data:
            if i['email'] == email:
                i['is_activated'] = True
                self.__file_worker.overwrite_file_by_path(path_to_file, data)
                return UserModel.create_response(200, "Ok")

    def delete_user(self, email):
        number_of_file = self.get_number_of_file(email)
        path_to_file = self.__file_worker.get_path_to_file(str(number_of_file))
        data = self.__file_worker.read_file(path_to_file)
        for i in data:
            if i['email'] == email:
                data.remove(i)
                self.__file_worker.overwrite_file_by_path(path_to_file, data)
                return UserModel.create_response(200, "Ok")
