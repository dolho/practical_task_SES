from itsdangerous import URLSafeTimedSerializer

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

SECRET_KEY=os.environ['SECRET_KEY']
SECURITY_PASSWORD_SALT=os.environ['SECURITY_PASSWORD_SALT']



def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    email = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    return email
