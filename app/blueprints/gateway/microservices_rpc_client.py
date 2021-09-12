from .interface_microservices_rpc_client import InterfaceMicroservicesRpcClient
import pika
import uuid
import json


class MicroservicesRpcClient(InterfaceMicroservicesRpcClient):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def call_for_currency_rate(self, jwt_token, from_currency="BTC", to="UAH"):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue_rates',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps({"request": "rate", "from": "BTC", "to": "UAH", "Authorization": jwt_token}))
        while self.response is None:
            self.connection.process_data_events()
        return self.response.decode("utf-8")

    def call_for_user(self, action, data: dict):
        body = {"request": action} | data
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue_user_auth',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(body))
        # TODO поменять routing key на получение из конфига
        while self.response is None:
            self.connection.process_data_events()
        return self.response.decode("utf-8")


    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body