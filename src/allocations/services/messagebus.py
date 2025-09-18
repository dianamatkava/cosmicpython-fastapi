from typing import List, Any

from src.allocations.domain import events as _events
from src.allocations.services import event_handler as _handler
from src.shared.uow import AbstractUnitOfWork


def send_out_of_stock_event(sku: str):
    # signal purchasing team to issue more batches
    print(f"OutOfStockEvent {sku=}")


# In-process bus (synchronous)
EVENT_HANDLER = {
    _events.OutOfStockEvent: [send_out_of_stock_event],
}


def handle_event(event: _events.Event):
    for handler in EVENT_HANDLER.get(type(event)):
        handler(**event.__dict__)


def dispatch(events: List[_events.Event]):
    for event in events:
        handle_event(event)


# ------------------------ v2 ------------------------

# In-process bus (synchronous)
EVENT_HANDLER_V2 = {
    _events.OutOfStockEvent: [_handler.send_out_of_stock_event],
    _events.BatchCreated: [_handler.send_out_of_stock_event],
    _events.AllocationRequired: [_handler.allocate],
}


def handle(uow: AbstractUnitOfWork, event: _events.Event) -> Any:  # TODO: temp
    queue = [event]
    res = []
    exceptions = []
    while queue:
        event = queue.pop(0)
        for handler in EVENT_HANDLER_V2.get(type(event), []):
            try:
                res.append(handler(uow, event))  # TODO: temp
            except Exception as e:
                exceptions.append(e)
            queue.extend(uow.collect_events())

    if exceptions:
        raise exceptions[0]
    return res[0]
