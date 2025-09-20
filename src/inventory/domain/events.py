from dataclasses import dataclass


class Event:
    """
    Events are immutable, historical facts indicating that a state change has occurred.
    They are broadcast using a publish-subscribe model, and the sender doesn't know
    who the recipients are.
    """


@dataclass
class OutOfStockEvent(Event):
    sku: str


@dataclass
class BatchQuantityChangedEvent(Event):
    ref: str
    qty: int
