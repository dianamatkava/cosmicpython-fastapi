from typing import Annotated

from fastapi import Depends

from src.orders.adapters.uow import OrderLineUnitOfWork
from src.orders.services.order_line_service import OrderLineService


def get_order_line_uow():
    return OrderLineUnitOfWork()


def get_order_line_service(
    uow: Annotated[OrderLineUnitOfWork, Depends(get_order_line_uow)],
):
    return OrderLineService(uow=uow)
