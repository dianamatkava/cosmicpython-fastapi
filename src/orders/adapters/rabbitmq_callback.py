"""
The Adapter layer is designed to import the domain logic it needs to execute,
this is not a code smell, this is acceptable and expected trade-off.
"""

import json
from typing import Type

from src.orders.adapters.uow.order_uow import OrderUnitOfWork
from src.orders.services.messagebus import handle, Message


def message_order_callback(message: Type[Message]):
    uow = OrderUnitOfWork()

    def message_handler(chanel, method, props, body):
        try:
            data = json.loads(body.decode("utf-8"))
            handle(uow, message(**data))
            chanel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as ex:
            print(ex)
            pass  # TODO: fault mechanism

    return message_handler
