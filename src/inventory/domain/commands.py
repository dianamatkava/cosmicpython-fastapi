from dataclasses import dataclass
from datetime import date
from typing import Optional


class Command:
    """
    Commands are imperative requests from one service to another,
    capturing the intent for an action. They are typically directed at a single recipient,
    and the sender expects a response (success or failure).
    """


@dataclass
class ChangeBatchQuantity(Command):
    ref: str
    qty: int


@dataclass
class AllocateOrderLine(Command):
    order_line_id: int


@dataclass
class DeallocateOrderLine(Command):
    order_line_id: int
    ref: str
