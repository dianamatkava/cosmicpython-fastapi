import time

from sqlalchemy.orm import clear_mappers

from src.adapters.redisclient import RedisClient
from src.inventory.adapters.uow import ProductAggregateUnitOfWork
from src.database.orm_mappers import start_mappers
from src.adapters.rabbitmqclient import RabbitMQClient
from src.config import Settings
from src.service_manager import service_manager
from src.shared.adapters.orm import OutboxStatus


def run():
    start_mappers()
    uow = ProductAggregateUnitOfWork()

    service_manager.startup(
        settings=Settings(),
        messaging_client=RabbitMQClient,
        mem_storage_client=RedisClient,
    )
    client = service_manager.get_messaging_client()

    while True:
        with uow as uow:
            events = uow.outbox_repo.list()
            for event in events:
                try:
                    client.publish(routing_key=event.routing_key, body=event.body)
                    event.status = OutboxStatus.SENT
                except Exception:
                    event.status = OutboxStatus.FAILED

            if events:
                uow.commit()

        time.sleep(1)


if __name__ == "__main__":
    try:
        run()
    except Exception as ex:
        print(ex)
        clear_mappers()
