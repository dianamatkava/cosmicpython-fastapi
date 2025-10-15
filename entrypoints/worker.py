import time

from src.adapters.rabbitmqclient import RabbitMQClient
from src.bootstrap import Bootstrap
from src.config import Settings


def run():
    while True:
        boot = Bootstrap().configure(
            settings=Settings(), messaging_client=RabbitMQClient
        )
        try:
            boot.startup()
        except Exception as e:
            boot.shutdown()
            print("worker crashed:", e, flush=True)
            time.sleep(5)


if __name__ == "__main__":
    run()
