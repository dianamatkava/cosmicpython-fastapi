from src.constants import Queues
from src.shared.domain.events import Command


class ChangeBatchQuantity(Command):
    _routing_key: str = Queues.CHANGE_BATCH_QUANTITY_COMMAND
    _aggregate_type: str = "ChangeBatchQuantity"
    ref: str
    qty: int


class AllocateOrderLine(Command):
    _routing_key: str = Queues.ALLOCATE_COMMAND
    _aggregate_type: str = "AllocateOrderLine"
    order_line_id: int


class DeallocateOrderLine(Command):
    _routing_key: str = Queues.DEALLOCATE_COMMAND
    _aggregate_type: str = "DeallocateOrderLine"
    order_line_id: int
    ref: str
