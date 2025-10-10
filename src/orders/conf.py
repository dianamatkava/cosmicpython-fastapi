from typing import Annotated

from fastapi import Depends

from src.orders.adapters.uow import OrderUnitOfWork
from src.orders.services.order_service import OrderService


def get_order_uow():
    return OrderUnitOfWork()


def get_order_service(
    uow: Annotated[OrderUnitOfWork, Depends(get_order_uow)],
) -> OrderService:
    return OrderService(uow=uow)
