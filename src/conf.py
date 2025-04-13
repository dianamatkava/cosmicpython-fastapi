from typing import Annotated, Any

from fastapi import Depends

from src.adapters.uow import UnitOfWork
from src.services.batch_service import BatchService


def get_unit_of_work() -> UnitOfWork:
    return UnitOfWork()


def get_batch_service(uof: Annotated[Any, Depends(get_unit_of_work)]) -> BatchService:
    return BatchService(uof=uof)
