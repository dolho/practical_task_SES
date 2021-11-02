import pika
import json
import os
from dotenv import load_dotenv, find_dotenv
from verification_handler import authorise
load_dotenv(find_dotenv())
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']


class RabbitMQHandler:
 # TODO добавить абстрактный класс
    def __init__(self, broker_url, currency_handler):
        self.__broker_url = broker_url
        self.__RABBITMQ_CONNECTION = pika.BlockingConnection(pika.URLParameters(self.__broker_url))
        self.__channel =  self.__RABBITMQ_CONNECTION.channel()
        self.__channel.queue_declare(queue='rpc_queue_rates')
        self.__channel.basic_qos(prefetch_count=1)
        self.__channel.basic_consume(queue='rpc_queue_rates', on_message_callback=self.currency_callback)

        self.__currency_handler = currency_handler
        # self.__CHANNEL_CONSUME_VACATIONS = RABBITMQ_CONNECTION.channel()
        # self.__vacation_consumer = self.__CHANNEL_CONSUME_VACATIONS.queue_declare(queue='currency_rate_rpc')
        # self.__CHANNEL_CONSUME_VACATIONS.queue_bind(exchange='currency_rate_rpc',
        #                                             queue='consume_currency_rates')
        # self.__CHANNEL_CONSUME_VACATIONS.basic_qos(prefetch_count=1)
        # self.__CHANNEL_CONSUME_VACATIONS.basic_consume(queue='consume_currency_rates', auto_ack=True,
        #                                         on_message_callback=self.currency_callback)
        #
        # self.__CHANNEL_PUBLISH_RATES = self.__RABBITMQ_CONNECTION.channel()
        # self.__CHANNEL_PUBLISH_RATES.exchange_declare(exchange='currency_rate_answer', exchange_type='fanout')

    def __get_rate_with_authorisation(self, parameters):
        answer = authorise(parameters.get("Authorization"))
        print(parameters)
        body = {}
        if answer.status == 200:
            body = self.__currency_handler.get_rate()
            body["status"] = 200
        else:
            body["status"] = answer.status
            body["message"] = answer.message
        return body

    def currency_callback(self, ch, method, properties, body):
        given_parameters = json.loads(body)
        body = self.__get_rate_with_authorisation(given_parameters)
        ch.basic_publish(exchange='',
                         routing_key=properties.reply_to,
                         properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                         body=json.dumps(body, default=str))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # self.__CHANNEL_PUBLISH_RATES.basic_publish(exchange='currency_rate_answer', routing_key='',
        #                                            body=json.dumps({"from": "BTC", "to": "UAH", "rate": 132}))

    def consume(self):
        self.__channel.start_consuming()


    def connect_to_rabbitmq(self):
        self.__RABBITMQ_CONNECTION = pika.BlockingConnection(pika.URLParameters(self.__broker_url))
        self.__channel = self.__RABBITMQ_CONNECTION.channel()

        self.__channel = self.__RABBITMQ_CONNECTION.channel()
        self.__channel.queue_declare(queue='rpc_queue_rates')
        self.__channel.basic_qos(prefetch_count=1)
        self.__channel.basic_consume(queue='rpc_queue_rates', on_message_callback=self.currency_callback)

    def check_connection(self):
        if self.__RABBITMQ_CONNECTION.is_open:
            pass
        else:
            self.connect_to_rabbitmq()