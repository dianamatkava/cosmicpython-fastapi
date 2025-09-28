import time

from adapters.rabbitmqclient import RabbitMQClient
from config import Settings
from service_manager import service_manager


def run():
    while True:
        try:
            service_manager.startup(settings=Settings(), messaging_client=RabbitMQClient)
            service_manager.define_queses()

            client = service_manager.get_messaging_client()
            client.startup()
        except Exception as e:
            print("worker crashed:", e, flush=True)
            time.sleep(5)


if __name__ == '__main__':
    run()
