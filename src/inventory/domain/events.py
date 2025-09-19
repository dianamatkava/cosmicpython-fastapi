from dataclasses import dataclass
from datetime import date
from typing import Optional


class Event:
    pass


@dataclass
class OutOfStockEvent(Event):
    sku: str


@dataclass
class BatchCreatedEvent(Event):
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None


@dataclass
class BatchQuantityChangedEvent(Event):
    ref: str
    qty: int


@dataclass
class AllocationRequiredEvent(Event):
    order_line_id: int


@dataclass
class DeallocateOrderLineEvent(Event):
    order_line_id: int
    ref: str
