import pika
import os
from rabbitmq_handler import RabbitMQHandler
from user_auth_registration_handler import UserAuthRegistrationHandler
from model import UserModel
from file_worker import FileWorker
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']


if __name__ == "__main__":
    print("Start consuming")
    user_handler = UserAuthRegistrationHandler(UserModel(FileWorker()))
    RABBITMQ_CONNECTION = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    # TODO перенести создание connection в RabbitMqHandler
    rabbitmq_handler = RabbitMQHandler(rabbitmq_connection=RABBITMQ_CONNECTION, user_handler=user_handler)
    rabbitmq_handler.consume()