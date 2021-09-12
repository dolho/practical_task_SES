import os
import jwt
from collections import namedtuple
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

SECRET_SALT = os.environ['SECRET_SALT']

VerificationAnswer = namedtuple('VerificationAnswer', 'status message')


def authorise(jwt_token) -> VerificationAnswer:
    if not jwt_token:
        return VerificationAnswer(401, "Unauthorized. No token give")
    try:
        payload = jwt.decode(jwt_token, SECRET_SALT, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        return VerificationAnswer(401, "Unauthorized. Token expired")
    except jwt.DecodeError:
        return VerificationAnswer(400, "Bad request. Invalid token")
    if not payload['is_activated']:
        return VerificationAnswer(401, "Unauthorized. Confirm your email first")
    return VerificationAnswer(200, "Ok")

