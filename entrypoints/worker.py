import time

from sqlalchemy.orm import clear_mappers

from src.adapters.redisclient import RedisClient
from src.database.orm_mappers import start_mappers
from src.adapters.rabbitmqclient import RabbitMQClient
from src.config import Settings
from src.service_manager import service_manager


def run():
    start_mappers()
    service_manager.startup(settings=Settings(), messaging_client=RabbitMQClient, mem_storage_client=RedisClient)
    service_manager.define_queses()

    client = service_manager.get_messaging_client()

    while True:
        try:
            client.startup()
        except Exception as e:
            clear_mappers()
            client.shutdown()
            print("worker crashed:", e, flush=True)
            time.sleep(5)


if __name__ == "__main__":
    run()
