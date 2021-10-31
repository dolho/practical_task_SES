from flask import Blueprint, request, Response
from .microservices_rpc_client import MicroservicesRpcClient
import pika
import json
import os
from flask.helpers import url_for
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

SECRET_SALT = os.environ['SECRET_SALT']
RABBITMQ_HOST = os.environ['CELERY_BROKER_URL']
blueprint_gateway = Blueprint('gateway', __name__)



connection = pika.BlockingConnection( pika.URLParameters(RABBITMQ_HOST))
# pika.ConnectionParameters(host=RABBITMQ_HOST)

CHANNEL_SEND = connection.channel()

CHANNEL_SEND.exchange_declare(exchange='rpc_queue_user_auth', exchange_type='fanout')
CHANNEL_SEND.exchange_declare(exchange='currency_rate', exchange_type='fanout')

# CHANNEL_CONSUME =

MICROSERVICE_RPC_CLIENT = MicroservicesRpcClient(RABBITMQ_HOST)

def form_response(result):
    print(result)
    if result.get("status") != 200:
        if result["message"] is not str:
            print(type(result["message"]))
            return Response(json.dumps(result["message"]), status=result["status"])
        return Response(result["message"], status=result["status"])
    else:
        if result["message"] is not str:
            print(type(result["message"]))
            return Response(json.dumps(result["message"]), status=result["status"])
        return Response(result["message"])

@blueprint_gateway.route('/btcRate', methods=['GET'])
def get_current_price():
    """returns current price of BTC in UAH
            ---
            tags:
              - Converter
            parameters:
              - name: Authorization
                in: header
                type: string
                required: true
            responses:
              200:
                description: returns price of BTC to UAH
                examples:

            """
    token = request.headers.get('Authorization')
    result = json.loads(MICROSERVICE_RPC_CLIENT.call_for_currency_rate(token))
    # CHANNEL_SEND.basic_publish(exchange='currency_rate', routing_key='', properties=pika.BasicProperties(
    #                         reply_to=callback_queue),
    # body=json.dumps({"request": "rate", "from": "BTC", "to": "UAH"}))
    return form_response(result)

@blueprint_gateway.route('/create', methods=['POST'])
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
          400:
            description: Given email or password is incorrect
        """
    email_confirmation_url = url_for("gateway.confirm_email", token="")
    user_data = {"email": request.headers['email'], "password": request.headers['password'],
                 "email_confirmation_url": request.host + "/" + email_confirmation_url}
    result = json.loads(MICROSERVICE_RPC_CLIENT.call_for_user("create", user_data))
    return form_response(result)


@blueprint_gateway.route('/login', methods=['POST'])
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
    user_data = {"email": request.headers['email'], "password": request.headers['password']}
    result = json.loads(MICROSERVICE_RPC_CLIENT.call_for_user("login", user_data))
    return form_response(result)


@blueprint_gateway.route('/confirm/<token>')
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
    user_data = {"token": token}
    result = json.loads(MICROSERVICE_RPC_CLIENT.call_for_user("confirm_email", user_data))
    return form_response(result)
