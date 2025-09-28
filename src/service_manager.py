from typing import TypeVar, Type

from src.inventory.adapters.rabbitmq_callbacks import create_message_callback
from src.inventory.domain import commands, events
from src.adapters.rabbitmqclient import MessagingClient
from src.config import Settings


# TODO: move somewhere else
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


T = TypeVar("T", bound=MessagingClient)


class ServiceManager(Singleton):
    _messaging_client: MessagingClient

    def startup(self, settings: Settings, messaging_client: Type[MessagingClient]):
        self._messaging_client = messaging_client(
            config=settings.MESSAGING_CLIENT
        )

    def define_queses(self):
        self._messaging_client.start_queue(queue_name="allocate", callback=create_message_callback(commands.AllocateOrderLine))
        self._messaging_client.start_queue(queue_name="deallocate", callback=create_message_callback(commands.DeallocateOrderLine))
        self._messaging_client.start_queue(
            queue_name="change_batch_quantity", callback=create_message_callback(commands.ChangeBatchQuantity)
        )
        self._messaging_client.start_queue(
            queue_name="out_of_stock_event", callback=create_message_callback(events.OutOfStockEvent)
        )
        self._messaging_client.start_queue(
            queue_name="batch_quantity_changed_event",
            callback=create_message_callback(events.BatchQuantityChangedEvent),
        )

    def shutdown(self):
        self._messaging_client.shutdown()

    def get_messaging_client(self):
        if self._messaging_client is None:
            raise RuntimeError("Messaging client is not initialized.")
        return service_manager._messaging_client


service_manager = ServiceManager()

