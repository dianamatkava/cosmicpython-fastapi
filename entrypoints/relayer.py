import time

from src.adapters.email import TwilioClient
from src.adapters.rabbitmqclient import RabbitMQClient
from src.adapters.redisclient import RedisClient
from src.bootstrap import Bootstrap
from src.config import Settings
from src.inventory.adapters.uow import ProductAggregateUnitOfWork
from src.shared.adapters.orm import OutboxStatus


def run():
    with Bootstrap().configure(
        settings=Settings(),
        uow=ProductAggregateUnitOfWork(),
        messaging_client=RabbitMQClient,
        mem_storage_client=RedisClient,
        notification_client=TwilioClient,
    ) as boot:
        pass

        while True:
            with boot.uow as uow:
                events = uow.outbox_repo.list()
                for event in events:
                    try:
                        boot.messaging_client.publish(
                            routing_key=event.routing_key, body=event.body
                        )
                        event.status = OutboxStatus.SENT
                    except Exception:
                        event.status = OutboxStatus.FAILED

                if events:
                    uow.commit()

            time.sleep(1)


if __name__ == "__main__":
    run()
