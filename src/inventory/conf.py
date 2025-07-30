from typing import Annotated, Any

from fastapi import Depends

from src.inventory.adapters.uow import InventoryBatchUnitOfWork, ProductUnitOfWork
from src.inventory.services.batch_service import BatchService
from src.inventory.services.product_service import ProductService


def get_batch_unit_of_work() -> InventoryBatchUnitOfWork:
    return InventoryBatchUnitOfWork()


def get_product_unit_of_work() -> ProductUnitOfWork:
    return ProductUnitOfWork()


def get_batch_service(
    uof: Annotated[Any, Depends(get_batch_unit_of_work)],
) -> BatchService:
    return BatchService(uow=uof)


def get_product_service(
    uow: Annotated[Any, Depends(get_product_unit_of_work)],
) -> ProductService:
    return ProductService(uow=uow)
