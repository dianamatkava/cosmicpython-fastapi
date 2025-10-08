from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

from src.adapters.redisclient import RedisClient
from src.service_manager import service_manager
from src.adapters.rabbitmqclient import RabbitMQClient
from src.config import Settings
from src.database.orm_mappers import start_mappers
from src.inventory.routes.views.batchs import router as batch_router
from src.inventory.routes.views.product import router as product_router
from src.inventory.routes.views.v1.allocations import router as allocations_router_v1
from src.inventory.routes.views.v2.allocations import router as allocations_router_v2
from src.orders.routes.order_line import router as order_line_router
from src.orders.routes.order import router as order_router


def _on_startup_event():
    clear_mappers()
    start_mappers()
    service_manager.startup(
        settings=Settings(),
        messaging_client=RabbitMQClient,
        mem_storage_client=RedisClient,
    )


def _on_shutdown_event():
    clear_mappers()
    service_manager.shutdown()


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(order_router)
    app.include_router(order_line_router)
    app.include_router(allocations_router_v1, prefix="/v1/sync")
    app.include_router(allocations_router_v2, prefix="/v2")
    app.include_router(batch_router)
    app.include_router(product_router)

    app.add_event_handler("startup", _on_startup_event)
    app.add_event_handler("shutdown", _on_shutdown_event)

    return app
