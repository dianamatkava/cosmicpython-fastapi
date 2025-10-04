from logging import getLogger
from typing import List, Dict, Type, Callable, Union

from src.inventory.domain import commands
from src.inventory.domain import events
from src.inventory.services import event_handler
from src.shared.log_codes import LogCode
from src.shared.uow import AbstractUnitOfWork

logger = getLogger(__name__)


EVENT_HANDLER: Dict[Type[events.DomainEvent], List[Callable]] = {
    events.OutOfStockEvent: [event_handler.send_out_of_stock_event],
    events.BatchQuantityChangedEvent: [event_handler.batch_quantity_changed_event],
}

COMMAND_HANDLER: Dict[Type[commands.Command], Callable] = {
    commands.AllocateOrderLine: event_handler.allocate,
    commands.DeallocateOrderLine: event_handler.deallocate,
    commands.ChangeBatchQuantity: event_handler.change_batch_quantity,
}

Message = Union[events.DomainEvent, commands.Command]


def handle(uow: AbstractUnitOfWork, message: Message) -> None:
    if isinstance(message, events.DomainEvent):
        handle_event(uow=uow, event=message)
    elif isinstance(message, commands.Command):
        handle_command(uow=uow, command=message)
    else:
        raise ValueError


def handle_event(uow: AbstractUnitOfWork, event: events.DomainEvent) -> None:
    for handler in EVENT_HANDLER.get(type(event), []):
        handler(uow, event)


def handle_command(uow: AbstractUnitOfWork, command: commands.Command) -> None:
    try:
        handler = COMMAND_HANDLER.get(type(command))
        handler(uow, command)
    except Exception as e:
        logger.error(
            "Event %s failed to execute",
            command,
            extra=dict(log_code=LogCode.COMMAND_FAILED),
            exc_info=True,
        )
        raise e
