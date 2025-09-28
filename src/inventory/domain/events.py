from dataclasses import dataclass

from pydantic import BaseModel


class Event(BaseModel):
    """
    Events are immutable, historical facts indicating that a state change has occurred.
    They are broadcast using a publish-subscribe model, and the sender doesn't know
    who the recipients are.
    """


class OutOfStockEvent(Event):
    sku: str


class BatchQuantityChangedEvent(Event):
    ref: str
    qty: int
