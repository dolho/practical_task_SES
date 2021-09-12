from celery import Celery
import smtplib, ssl
import email.message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
# mail = Mail(current_app)

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_BACKEND_RPC = os.environ['CELERY_BACKEND_RPC']
# TODO Поменять на переменные окружения

app = Celery('email_worker', broker=CELERY_BROKER_URL,  backend=CELERY_BACKEND_RPC)

PORT = 465  # For SSL
LOGIN = os.environ['MAIL_USERNAME']
PASSWORD = os.environ['MAIL_PASSWORD']
CONTEXT = ssl.create_default_context()


# Create a secure SSL context
context = ssl.create_default_context()


#
@app.task(name='app.blueprints.user.email_worker.send_confirmation_email')
def send_confirmation_email(user_email, token_link):
    m = MIMEMultipart("alternative")
    m['From'] = LOGIN
    m['To'] = user_email
    m['Subject'] = "Email confirmation"
    text = f'Visit {token_link} to activate your account. Ignore the message if you didn\'t register'

    part1 = MIMEText(text, "plain")
    # TODO Email shows the same text twice; for some reason, 10minutemail changes link, so it becomes unclickable
    part2 = MIMEText(
        f'Click <a href="{token_link}">here</a> to confirm your email. Ignore this message if you didn\'t register'
        f' or visit this link {token_link} ',
        'html')

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    m.attach(part1)
    # m.attach(part2)
    with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
        server.login(LOGIN, PASSWORD)
        server.sendmail(LOGIN, user_email, m.as_string())


# @app.task(name='app.blueprints.user.email_worker.i_am_mail')
# def i_am_mail(email, msg):
#     print(f"I've recived ypour message, and now I will save it into db {email}, {msg}")