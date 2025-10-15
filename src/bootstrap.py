from typing import Type, Optional

from sqlalchemy.orm import clear_mappers

from src.adapters.email import NotificationClient
from src.adapters.rabbitmqclient import MessagingClient
from src.adapters.redisclient import MemStorageClient
from src.config import Settings
from src.constants import Queues
from src.database.orm_mappers import start_mappers
from src.inventory.adapters.rabbitmq_callbacks import message_product_callback
from src.inventory.domain.commands import (
    ChangeBatchQuantity,
    DeallocateOrderLine,
    AllocateOrderLine,
)
from src.inventory.domain.events import OutOfStockEvent, BatchQuantityChangedEvent
from src.orders.adapters.rabbitmq_callback import message_order_callback
from src.orders.domain.events import (
    OrderShipped,
    OrderPayed,
    OrderStatusChanged,
    OrderLineRemoved,
    OrderLineAdded,
    OrderCreated,
)
from src.shared.adapters.uow import AbstractUnitOfWork


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


class Bootstrap(Singleton):
    """
    Bootstrap can be used as:
      - a singleton (module-level) with boot.configure(...) and boot.startup()/shutdown()
      - a short-lived context: `with Bootstrap(... ) as boot:`
    Features:
      - startup() is idempotent
      - shutdown() is idempotent
      - factories may be callables that receive `bootstrap` as single argument (for recursive deps)
    """

    _messaging_client: Optional[MessagingClient] = None
    _mem_storage_client: Optional[MemStorageClient] = None
    _notification_client: Optional[NotificationClient] = None

    def __init__(self):
        self.settings = None
        self.define_queues = False
        self.messaging_client_cls = None
        self.mem_storage_client_cls = None
        self.notification_client_cls = None
        self.uow = None
        self.with_mappers = False
        self._started = False

    def configure(
        self,
        settings: Settings,
        messaging_client: Optional[Type[MessagingClient]] = None,
        mem_storage_client: Optional[Type[MemStorageClient]] = None,
        notification_client: Optional[Type[NotificationClient]] = None,
        uow: Optional[AbstractUnitOfWork] = None,
        with_mappers: bool = True,
        define_queues: bool = True,
    ):
        self.uow = uow
        self.messaging_client_cls = messaging_client
        self.mem_storage_client_cls = mem_storage_client
        self.notification_client_cls = notification_client
        self.with_mappers = with_mappers
        self.define_queues = define_queues
        self.settings = settings
        self._started = True

    def __enter__(self):
        self.startup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def startup(self):
        # TODO: make it idempotent
        if not self._started:
            raise RuntimeError("Bootstrap must be configured first.")
        if self.with_mappers:
            start_mappers()
        if self.messaging_client_cls:
            self._messaging_client = self.messaging_client_cls(
                config=self.settings.MESSAGING_CLIENT
            )
            self.define_queses()
        if self.mem_storage_client_cls:
            self._mem_storage_client = self.mem_storage_client_cls(
                config=self.settings.MEM_STORAGE_CLIENT
            )
        if self.notification_client_cls:
            self._notification_client = self.notification_client_cls(
                config=self.settings.NOTIFICATION_CLIENT
            )

    def shutdown(self):
        # TODO: make it idempotent
        if self.with_mappers:
            clear_mappers()
        if self.messaging_client_cls:
            self._messaging_client.shutdown()
        if self.mem_storage_client_cls:
            self._mem_storage_client.shutdown()
        if self.notification_client_cls:
            self._notification_client.shutdown()

    @property
    def messaging_client(self) -> MessagingClient:
        if not self._messaging_client:
            print("ERROR: Messaging client not set up")
        return self._messaging_client

    @property
    def mem_storage_client(self) -> MemStorageClient:
        if not self._mem_storage_client:
            print("ERROR: in-Mem Storage client not set up")
        return self._mem_storage_client

    @property
    def notification_client(self) -> NotificationClient:
        if not self._notification_client:
            print("ERROR: Notification client not set up")
        return self._notification_client

    def define_queses(self):
        self.messaging_client.start_queue(
            queue_name=Queues.ORDER_CREATED_EVENT,
            callback=message_order_callback(OrderCreated),
        )
        self.messaging_client.start_queue(
            queue_name=Queues.ORDER_LINE_ADDED_EVENT,
            callback=message_order_callback(OrderLineAdded),
        )
        self.messaging_client.start_queue(
            queue_name=Queues.ORDER_LINE_REMOVED_EVENT,
            callback=message_order_callback(OrderLineRemoved),
        )
        self.messaging_client.start_queue(
            queue_name=Queues.ORDER_STATUS_CHANGE_EVENT,
            callback=message_order_callback(OrderStatusChanged),
        )
        self.messaging_client.start_queue(
            queue_name=Queues.ORDER_PAYED_EVENT,
            callback=message_order_callback(OrderPayed),
        )
        self.messaging_client.start_queue(
            queue_name=Queues.ORDER_SHIPPED_EVENT,
            callback=message_order_callback(OrderShipped),
        )
        self.messaging_client.start_queue(
            queue_name=Queues.ALLOCATE_COMMAND,
            callback=message_product_callback(AllocateOrderLine),
        )
        self.messaging_client.start_queue(
            queue_name=Queues.DEALLOCATE_COMMAND,
            callback=message_product_callback(DeallocateOrderLine),
        )
        self.messaging_client.start_queue(
            queue_name=Queues.CHANGE_BATCH_QUANTITY_COMMAND,
            callback=message_product_callback(ChangeBatchQuantity),
        )
        self.messaging_client.start_queue(
            queue_name=Queues.OUT_OF_STOCK_EVENT,
            callback=message_product_callback(OutOfStockEvent),
        )
        self.messaging_client.start_queue(
            queue_name=Queues.BATCH_QUANTITY_CHANGED_EVENT,
            callback=message_product_callback(BatchQuantityChangedEvent),
        )


boot = Bootstrap()
