from typing import Annotated

from fastapi import Depends

from src.orders.adapters.uow.order_line_uow import OrderLineUnitOfWork
from src.orders.adapters.uow.order_uow import OrderUnitOfWork
from src.orders.services.order_line_service import OrderLineService
from src.orders.services.order_service import OrderService


def get_order_line_uow():
    return OrderLineUnitOfWork()


def get_order_uow():
    return OrderUnitOfWork()


def get_order_line_service(
    uow: Annotated[OrderLineUnitOfWork, Depends(get_order_line_uow)],
) -> OrderLineService:
    return OrderLineService(uow=uow)


def get_order_service(
    uow: Annotated[OrderUnitOfWork, Depends(get_order_uow)],
) -> OrderService:
    return OrderService(uow=uow)
