import time

from sqlalchemy.orm import clear_mappers

from src.database.orm_mappers import start_mappers
from src.adapters.rabbitmqclient import RabbitMQClient
from src.config import Settings
from src.service_manager import service_manager


def run():
    start_mappers()
    while True:
        try:
            service_manager.startup(
                settings=Settings(), messaging_client=RabbitMQClient
            )
            service_manager.define_queses()

            client = service_manager.get_messaging_client()
            client.startup()
        except Exception as e:
            clear_mappers()
            print("worker crashed:", e, flush=True)
            time.sleep(5)


if __name__ == "__main__":
    run()
