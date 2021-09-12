import abc

class InterfaceMicroservicesRpcClient(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'call_for_currency_rate') and
                callable(subclass.load_data_source) and
                hasattr(subclass, 'on_response') and
                callable(subclass.extract_text) or
                NotImplemented)


    @abc.abstractmethod
    def call_for_currency_rate(self, from_currency="BTC", to="UAH"):
        raise NotImplementedError



    @abc.abstractmethod
    def on_response(self, ch, method, props, body):
        raise NotImplementedError
