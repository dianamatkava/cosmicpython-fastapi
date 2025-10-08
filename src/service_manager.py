from typing import TypeVar, Type

from src.adapters.rabbitmqclient import MessagingClient
from src.adapters.redisclient import MemStorageClient
from src.config import Settings
from src.constants import Queues
from src.inventory.adapters.rabbitmq_callbacks import message_product_callback
from src.inventory.domain.commands import (
    AllocateOrderLine,
    DeallocateOrderLine,
    ChangeBatchQuantity,
)
from src.inventory.domain.events import OutOfStockEvent, BatchQuantityChangedEvent
from src.orders.adapters.rabbitmq_callback import message_order_callback
from src.orders.domain.events import (
    OrderCreated,
    OrderLineAdded,
    OrderLineRemoved,
    OrderStatusChanged,
    OrderPayed,
    OrderShipped,
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
    _messaging_client: MessagingClient
    _mem_storage_client: MemStorageClient

    def startup(
        self,
        settings: Settings,
        messaging_client: Type[MessagingClient],
        mem_storage_client: Type[MemStorageClient],
    ):
        self._messaging_client = messaging_client(config=settings.MESSAGING_CLIENT)
        self._mem_storage_client = mem_storage_client(config=settings.MEM_STORAGE)

    def define_queses(self):
        self._messaging_client.start_queue(
            queue_name=Queues.ORDER_CREATED_EVENT,
            callback=message_order_callback(OrderCreated),
        )
        self._messaging_client.start_queue(
            queue_name=Queues.ORDER_LINE_ADDED_EVENT,
            callback=message_order_callback(OrderLineAdded),
        )
        self._messaging_client.start_queue(
            queue_name=Queues.ORDER_LINE_REMOVED_EVENT,
            callback=message_order_callback(OrderLineRemoved),
        )
        self._messaging_client.start_queue(
            queue_name=Queues.ORDER_STATUS_CHANGE_EVENT,
            callback=message_order_callback(OrderStatusChanged),
        )
        self._messaging_client.start_queue(
            queue_name=Queues.ORDER_PAYED_EVENT,
            callback=message_order_callback(OrderPayed),
        )
        self._messaging_client.start_queue(
            queue_name=Queues.ORDER_SHIPPED_EVENT,
            callback=message_order_callback(OrderShipped),
        )

        self._messaging_client.start_queue(
            queue_name=Queues.ALLOCATE_COMMAND,
            callback=message_product_callback(AllocateOrderLine),
        )
        self._messaging_client.start_queue(
            queue_name=Queues.DEALLOCATE_COMMAND,
            callback=message_product_callback(DeallocateOrderLine),
        )
        self._messaging_client.start_queue(
            queue_name=Queues.CHANGE_BATCH_QUANTITY_COMMAND,
            callback=message_product_callback(ChangeBatchQuantity),
        )
        self._messaging_client.start_queue(
            queue_name=Queues.OUT_OF_STOCK_EVENT,
            callback=message_product_callback(OutOfStockEvent),
        )
        self._messaging_client.start_queue(
            queue_name=Queues.BATCH_QUANTITY_CHANGED_EVENT,
            callback=message_product_callback(BatchQuantityChangedEvent),
        )

    def shutdown(self):
        self._messaging_client.shutdown()
        self._mem_storage_client.shutdown()

    def get_messaging_client(self) -> MessagingClient:
        if self._messaging_client is None:
            raise RuntimeError("Messaging client is not initialized.")
        return service_manager._messaging_client

    def get_mem_storage_client(self) -> MemStorageClient:
        if self._mem_storage_client is None:
            raise RuntimeError("In memory storage client is not initialized.")
        return service_manager._mem_storage_client


service_manager = ServiceManager()
