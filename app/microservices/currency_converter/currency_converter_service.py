import pika
import os
from rabbitmq_handler import RabbitMQHandler
from save_cache import CacheHandler
from coinbase_handler import CoinbaseHandler
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
RABBITMQ_HOST = os.environ['CELERY_BROKER_URL']


if __name__ == "__main__":
    print("Start consuming")
    RABBITMQ_CONNECTION = pika.BlockingConnection(pika.URLParameters(RABBITMQ_HOST))
    # TODO перенести создание connection в RabbitMqHandler
    cache_handler = CacheHandler()
    currency_handler = CoinbaseHandler(cache_handler)
    rabbitmq_handler = RabbitMQHandler(rabbitmq_connection=RABBITMQ_CONNECTION, currency_handler=currency_handler)
    rabbitmq_handler.consume()