from dataclasses import dataclass


class Event:
    pass


@dataclass
class OutOfStockEvent(Event):
    sku: str
