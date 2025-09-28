from logging import getLogger
from typing import List, Any, Dict, Type, Callable, Union

from src.inventory.domain import commands
from src.inventory.domain import events
from src.inventory.services import event_handler
from src.shared.log_codes import LogCode
from src.shared.uow import AbstractUnitOfWork

logger = getLogger(__name__)

EVENT_HANDLER: Dict[Type[events.Event], List[Callable]] = {
    events.OutOfStockEvent: [event_handler.send_out_of_stock_event],
    events.BatchQuantityChangedEvent: [event_handler.batch_quantity_changed_event],
}

COMMAND_HANDLER: Dict[Type[commands.Command], Callable] = {
    commands.AllocateOrderLine: event_handler.allocate,
    commands.DeallocateOrderLine: event_handler.deallocate,
    commands.ChangeBatchQuantity: event_handler.change_batch_quantity,
}

Message = Union[events.Event, commands.Command]


# ---------------------- In process message bus (sync approach) ----------------------
def handle(uow: AbstractUnitOfWork, message: Message) -> Any:
    queue = [message]
    res = []
    while queue:
        message = queue.pop(0)
        if isinstance(message, events.Event):
            handle_event(uow=uow, event=message)
        elif isinstance(message, commands.Command):
            res.append(handle_command(uow=uow, command=message))
        else:
            raise ValueError

        queue.extend(uow.collect_events())

    return res[0]


def handle_event(uow: AbstractUnitOfWork, event: events.Event) -> None:
    for handler in EVENT_HANDLER.get(type(event), []):
        try:
            handler(uow, event)
        except Exception:
            logger.error(
                "Event %s failed to execute",
                event,
                extra=dict(log_code=LogCode.EVENT_FAILED),
                exc_info=True,
            )


def handle_command(uow: AbstractUnitOfWork, command: commands.Command) -> Any:
    try:
        handler = COMMAND_HANDLER.get(type(command))
        res = handler(uow, command)
        return res
    except Exception as e:
        logger.error(
            "Event %s failed to execute",
            command,
            extra=dict(log_code=LogCode.COMMAND_FAILED),
            exc_info=True,
        )
        raise e
