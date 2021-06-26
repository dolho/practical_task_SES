from flask import Blueprint, request, Response
from . import model
from .token import confirm_token




blueprint_user = Blueprint('user', __name__, url_prefix='/user')

# Set the route and accepted methods
@blueprint_user.route('/create', methods=['POST'])
def create_user():
    """
    Creates new user
        ---
        tags:
          - User
        parameters:
          - name: email
            in: header
            type: string
            format: email
            required: true
          - name: password
            in: header
            type: string
            format: password
            required: true
        responses:
          200:
            description: Returns "True", if successful

            examples:
              rgb: 'True'
          400:
            description: Given email or password is incorrect
        """
    try:
        model.create_user(request.headers['email'], request.headers['password'], request.host)
    except KeyError:
        return Response("Bad request", status=400)
    except ValueError:
        return Response("Email is already used", status=400)
    return 'Ok'


@blueprint_user.route('/login', methods=['POST'])
def login():
    """
    Logins user
            ---
            tags:
              - User
            parameters:
              - name: email
                in: header
                type: string
                format: email
                required: true
              - name: password
                in: header
                type: string
                format: password
                required: true
            definitions:
              JWT-token:
                type: string
                example: xxxxx.yyyyy.zzzzz
            responses:
              '200':
                description: Returns jwt token, if login is successful
                content:
                  application/json:
                    schema:
                      type: string
              401:
                description: Given password is incorrect
              404:
                description: Given email is not found
            """
    jwt_token = model.login_user(request.headers['email'], request.headers['password'])
    return jwt_token


@blueprint_user.route('/confirm/<token>')
def confirm_email(token):
    """
    Confirms user email by token, which are sent to user email
                ---
                tags:
                  - User
                parameters:
                  - name: token
                    in: path
                    type: string
                    required: true
                responses:
                  '200':
                    description: Returns Ok, if user activated
                    content:
                      application/json:
                        schema:
                          type: string
                  401:
                    description: Confirmation link expired
                  404:
                    description: User with such email not found
                """
    try:
        email = confirm_token(token)
    except:
        return Response('Your confirmation link expired', status=401)
    try:
        model.activate_account(email)
    except FileNotFoundError:
        return Response('Internal server error. User with such email not found', status=404)
    return 'Ok'
