from typing import Annotated

from fastapi import Depends

from src.inventory.adapters.uow import ProductAggregateUnitOfWork
from src.inventory.services.batch_service import BatchService
from src.inventory.services.product_service import ProductService


def get_unit_of_work() -> ProductAggregateUnitOfWork:
    return ProductAggregateUnitOfWork()


def get_batch_service(
    uow: Annotated[ProductAggregateUnitOfWork, Depends(get_unit_of_work)],
) -> BatchService:
    return BatchService(uow=uow)


def get_product_service(
    uow: Annotated[ProductAggregateUnitOfWork, Depends(get_unit_of_work)],
) -> ProductService:
    return ProductService(uow=uow)
