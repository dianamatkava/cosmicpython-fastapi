"""
The Adapter layer is designed to import the domain logic it needs to execute,
this is not a code smell, this is acceptable and expected trade-off.
"""

import json
from typing import Type

from src.inventory.adapters.uow import ProductAggregateUnitOfWork
from src.inventory.services.messagebus import Message, handle


def message_product_callback(message: Type[Message]):
    uow = ProductAggregateUnitOfWork()

    def message_handler(chanel, method, props, body):
        try:
            data = json.loads(body.decode("utf-8"))
            handle(uow, message(**data))
            chanel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as ex:
            print(ex)
            pass  # TODO: fault mechanism

    return message_handler
