from datetime import datetime

from pydantic import BaseModel


class Command(BaseModel):
    """
    Commands are imperative requests from one service to another,
    capturing the intent for an action. They are typically directed at a single recipient,
    and the sender expects a response (success or failure).
    """

    _routing_key: str = "Unknown"
    _aggregate_type: str = "Generic"
    aggregate_id: str = "NaN"
    occurred_on: datetime = datetime.utcnow()

    @property
    def routing_key(self):
        return self._routing_key

    @property
    def aggregate_type(self):
        return self._aggregate_type


class ChangeBatchQuantity(Command):
    _routing_key: str = "change_batch_quantity"
    _aggregate_type: str = "ChangeBatchQuantity"
    ref: str
    qty: int


class AllocateOrderLine(Command):
    _routing_key: str = "allocate"
    _aggregate_type: str = "AllocateOrderLine"
    order_line_id: int


class DeallocateOrderLine(Command):
    _routing_key: str = "deallocate"
    _aggregate_type: str = "DeallocateOrderLine"
    order_line_id: int
    ref: str
