from typing import Annotated, Any

from fastapi import Depends

from src.allocations.adapters.uow import AllocationsUnitOfWork
from src.allocations.services.batch_service import BatchService


def get_unit_of_work() -> AllocationsUnitOfWork:
    return AllocationsUnitOfWork()


def get_batch_service(uof: Annotated[Any, Depends(get_unit_of_work)]) -> BatchService:
    return BatchService(uow=uof)
