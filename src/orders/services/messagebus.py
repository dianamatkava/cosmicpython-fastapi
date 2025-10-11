import logging
from typing import Dict, Callable, Union, List, Type

from src.orders.domain.events import (
    OrderCreated,
    OrderLineAdded,
    OrderLineRemoved,
    OrderPayed,
    OrderStatusChanged,
    OrderShipped,
)
from src.orders.services.event_handlers import (
    order_line_added_event,
    order_line_removed_event,
    order_status_changed_notify_event,
    order_payed_notify_event,
    order_shipped_notify_event, order_line_created_event_db, order_created_event_email, order_line_created_event_mem,
)
from src.shared.domain.events import Event, Command
from src.constants import LogCode
from src.shared.uow import AbstractUnitOfWork


logger = logging.getLogger(__name__)


EVENT_HANDLERS: Dict[Type[Event], List[Callable]] = {
    OrderCreated: [order_created_event_email],
    OrderLineAdded: [
        order_line_created_event_db,
        order_line_created_event_mem,
    ],
    OrderLineRemoved: [order_line_removed_event],

    OrderStatusChanged: [order_status_changed_notify_event],
    OrderPayed: [order_payed_notify_event],
    OrderShipped: [order_shipped_notify_event],
}

COMMAND_HANDLER: Dict[Type[Command], List[Callable]] = {}

Message = Union[Event, Command]


def handle(uow: AbstractUnitOfWork, message: Message):
    if isinstance(message, Event):
        handle_event(uow=uow, event=message)
    elif isinstance(message, Event):
        handle_event(uow=uow, event=message)
    else:
        ValueError("Message is invalid type")


def handle_event(uow: AbstractUnitOfWork, event: Event) -> None:
    events = EVENT_HANDLERS.get(type(event), [])

    if not events:
        ValueError("Event not found")

    for handler in events:
        handler(uow=uow, event=event)


def handle_command(uow: AbstractUnitOfWork, command: Command) -> None:
    try:
        handler = COMMAND_HANDLER.get(type(command))
        handler(uow=uow, command=command)
    except Exception:
        logger.error(
            "Event %s failed to execute",
            command,
            extra=dict(log_code=LogCode.COMMAND_FAILED),
            exc_info=True,
        )
