import pika
import json


class RabbitMQHandler:
 # TODO добавить абстрактный класс


    def __init__(self, rabbitmq_connection, user_handler):
        self.__RABBITMQ_CONNECTION = rabbitmq_connection
        self.__channel =  self.__RABBITMQ_CONNECTION.channel()
        self.__channel.queue_declare(queue='rpc_queue_user_auth')
        #TODO Вынести в кофиг
        self.__channel.basic_qos(prefetch_count=1)
        self.__channel.basic_consume(queue='rpc_queue_user_auth', on_message_callback=self.user_callback)

        self.__user_handler = user_handler
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


    def user_callback(self, ch, method, properties, body):
        given_parameters = json.loads(body)
        body = self.__user_handler.route(given_parameters)
        ch.basic_publish(exchange='',
                         routing_key=properties.reply_to,
                         properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                         body=json.dumps(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # self.__CHANNEL_PUBLISH_RATES.basic_publish(exchange='currency_rate_answer', routing_key='',
        #                                            body=json.dumps({"from": "BTC", "to": "UAH", "rate": 132}))

    def consume(self):
        self.__channel.start_consuming()