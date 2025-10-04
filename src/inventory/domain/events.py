from src.constants import Queues
from src.shared.domain.events import Event


class OutOfStockEvent(Event):
    _routing_key: str = Queues.OUT_OF_STOCK_EVENT
    _aggregate_type: str = "OutOfStockEvent"
    sku: str


class BatchQuantityChangedEvent(Event):
    _routing_key: str = Queues.BATCH_QUANTITY_CHANGED_EVENT
    _aggregate_type: str = "BatchQuantityChangedEvent"
    ref: str
    qty: int
