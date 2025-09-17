from typing import List

from src.allocations.domain import events as _events


def send_out_of_stock_event(sku: str):
    # signal purchasing team to issue more batches
    print(f"OutOfStockEvent {sku=}")


# In-process bus (synchronous)
EVENT_HANDLER = {_events.OutOfStockEvent: [send_out_of_stock_event]}


def handle_event(event: _events.Event):
    for handler in EVENT_HANDLER.get(type(event)):
        handler(**event.__dict__)


def dispatch(events: List[_events.Event]):
    for event in events:
        handle_event(event)
