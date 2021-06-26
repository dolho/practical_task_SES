from flask import Blueprint, request, Response
import requests
import threading
import time
import datetime
import jwt

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

SECRET_SALT = os.environ['SECRET_SALT']

RATE = {}

def requests_thread():
    global RATE
    while True:
        r = requests.get('https://api.coinbase.com/v2/prices/BTC-UAH/buy')
        rate = r.json()['data']
        rate['time'] = datetime.datetime.now()
        RATE = rate.copy()
        time.sleep(60)

x = threading.Thread(target=requests_thread)
x.daemon = True
x.start()

blueprint_converter = Blueprint('converter', __name__)
SECRET_SALT = "salty_daf244"

@blueprint_converter.route('/btcRate', methods=['GET'])
def get_current_price():
    """Example endpoint returning a list of colors by palette
            This is using docstrings for specifications.
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
                  rgb: 'True'
            """
    token = request.headers.get('Authorization')
    if not token:
        return Response("Unauthorized. No token given", status=401)
    try:
        payload = jwt.decode(token, SECRET_SALT, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        return Response("Unauthorized. Token expired", status=401)
    except jwt.DecodeError:
        return Response("Bad request. Invalid token", status=400)
    if not payload['is_activated']:
        return Response("Unauthorized. Confirm your email first", status=401)
    return RATE