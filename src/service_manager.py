from typing import TypeVar, Type

from src.adapters.rabbitmqclient import MessagingClient
from src.config import Settings
from src.inventory.services.event_handler import (
    allocate,
    deallocate,
    change_batch_quantity,
    send_out_of_stock_event,
    batch_quantity_changed_event,
)


# TODO: move somewhere else
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


T = TypeVar("T", bound=MessagingClient)


class ServiceManager(Singleton):
    messaging_client: MessagingClient

    def startup(self, settings: Settings, messaging_client: Type[T]):
        self.messaging_client = messaging_client(
            config=settings.MESSAGING_CLIENT
        ).startup()

    def define_queses(self):
        self.messaging_client.start_queue(queue_name="allocate", callback=allocate)
        self.messaging_client.start_queue(queue_name="deallocate", callback=deallocate)
        self.messaging_client.start_queue(
            queue_name="change_batch_quantity", callback=change_batch_quantity
        )
        self.messaging_client.start_queue(
            queue_name="send_out_of_stock_event", callback=send_out_of_stock_event
        )
        self.messaging_client.start_queue(
            queue_name="batch_quantity_changed_event",
            callback=batch_quantity_changed_event,
        )

    def shutdown(self):
        self.messaging_client.shutdown()


service_manager = ServiceManager()
