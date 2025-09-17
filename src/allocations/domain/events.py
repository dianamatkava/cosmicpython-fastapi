from dataclasses import dataclass
from datetime import date
from typing import Optional


class Event:
    pass


@dataclass
class OutOfStockEvent(Event):
    sku: str


@dataclass
class BatchCreated(Event):
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None


@dataclass
class BatchQuantityChanged(Event):
    ref: str
    qty: int


@dataclass
class AllocationRequired(Event):
    order_line_id: int  # TODO: allocate entire order
