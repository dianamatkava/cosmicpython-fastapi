from pydantic import BaseModel


class Command(BaseModel):
    """
    Commands are imperative requests from one service to another,
    capturing the intent for an action. They are typically directed at a single recipient,
    and the sender expects a response (success or failure).
    """


class ChangeBatchQuantity(Command):
    ref: str
    qty: int


class AllocateOrderLine(Command):
    order_line_id: int


class DeallocateOrderLine(Command):
    order_line_id: int
    ref: str
