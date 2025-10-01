"""
The Adapter layer is designed to import the domain logic it needs to execute,
this is not a code smell, this is acceptable and expected trade-off.
"""

import json
import logging
from logging.handlers import RotatingFileHandler
from typing import Type

from src.inventory.services.messagebus import Message, handle
from src.inventory.adapters.uow import ProductAggregateUnitOfWork

LOG_PATH = "./app.log"

logger = logging.getLogger("consumer")
logger.setLevel(logging.INFO)

fh = RotatingFileHandler(LOG_PATH, maxBytes=10_000_000, backupCount=5)
fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
logger.addHandler(fh)


def test(chanel, method, props, body):
    logger.error("HELLLO _______________>>>>>>>>>>>>>>")
    print(chanel, method, props, body, flush=True)
    chanel.basic_ack(delivery_tag=method.delivery_tag)


def create_message_callback(message: Type[Message]):
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
