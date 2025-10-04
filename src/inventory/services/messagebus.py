from logging import getLogger
from typing import List, Dict, Type, Callable, Union

from src.inventory.domain.commands import (
    ChangeBatchQuantity,
    DeallocateOrderLine,
    AllocateOrderLine,
)
from src.inventory.domain.events import BatchQuantityChangedEvent, OutOfStockEvent
from src.inventory.services import event_handler
from src.shared.domain.events import Command, Event
from src.constants import LogCode
from src.shared.uow import AbstractUnitOfWork

logger = getLogger(__name__)


EVENT_HANDLER: Dict[Type[Event], List[Callable]] = {
    OutOfStockEvent: [event_handler.send_out_of_stock_event],
    BatchQuantityChangedEvent: [event_handler.batch_quantity_changed_event],
}

COMMAND_HANDLER: Dict[Type[Command], Callable] = {
    AllocateOrderLine: event_handler.allocate,
    DeallocateOrderLine: event_handler.deallocate,
    ChangeBatchQuantity: event_handler.change_batch_quantity,
}

Message = Union[Event, Command]


def handle(uow: AbstractUnitOfWork, message: Message) -> None:
    if isinstance(message, Event):
        handle_event(uow=uow, event=message)
    elif isinstance(message, Command):
        handle_command(uow=uow, command=message)
    else:
        raise ValueError("Message is invalid type")


def handle_event(uow: AbstractUnitOfWork, event: Event) -> None:
    for handler in EVENT_HANDLER.get(type(event), []):
        handler(uow, event)


def handle_command(uow: AbstractUnitOfWork, command: Command) -> None:
    try:
        handler = COMMAND_HANDLER.get(type(command))
        handler(uow, command)
    except Exception:
        logger.error(
            "Event %s failed to execute",
            command,
            extra=dict(log_code=LogCode.COMMAND_FAILED),
            exc_info=True,
        )
