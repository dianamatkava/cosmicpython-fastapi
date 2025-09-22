from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

from src.adapters.rabbitmqclient import RabbitMQClient
from src.config import Settings
from src.database.orm_mappers import start_mappers
from src.inventory.routes.views.allocations import router as allocations_router
from src.inventory.routes.views.batchs import router as batch_router
from src.inventory.routes.views.product import router as product_router
from src.orders.routes.order_line import router as order_line_router
from src.service_manager import service_manager


def _on_startup_event():
    clear_mappers()
    start_mappers()
    service_manager.startup(settings=Settings(), messaging_client=RabbitMQClient)
    service_manager.define_queses()


def _on_shutdown_event():
    clear_mappers()
    service_manager.shutdown()


def create_app():
    app = FastAPI()

    app.include_router(order_line_router)
    app.include_router(allocations_router)
    app.include_router(batch_router)
    app.include_router(product_router)

    app.add_event_handler("startup", _on_startup_event)
    app.add_event_handler("shutdown", _on_startup_event)
