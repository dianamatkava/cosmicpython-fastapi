from abc import abstractmethod, ABC
from typing import Callable

import pika
from pika.adapters.blocking_connection import BlockingChannel

from src.config import MessagingClientSettings


# TODO: move somewhere else
class MessagingClient(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def startup(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def start_queue(self, queue_name: str, callback: callable):
        pass


class RabbitMQClient(MessagingClient):
    channel: BlockingChannel

    def __init__(self, config: MessagingClientSettings):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.host)
        )
        self.channel = connection.channel()
        # set prefetch_count so then one worker does not take a bulk of all tasks.
        # basic quality of service fare dispatch mechanism
        self.channel.basic_qos(
            prefetch_count=config.prefetch_count
        )  # Specifies a prefetch window in terms of whole messages

    def startup(self):
        self.channel.start_consuming()
        return self

    def shutdown(self):
        self.channel.stop_consuming()

    def create_queue(self, queue_name: str, durable: bool = True):
        self.channel.queue_declare(queue_name, durable=durable)

    def consume_queue(self, queue_name: str, callback: Callable):
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback)

    def start_queue(self, queue_name: str, callback: Callable, durable: bool = True):
        self.channel.queue_declare(queue_name, durable=durable)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback)
