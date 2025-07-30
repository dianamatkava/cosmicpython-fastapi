from typing import Annotated, Any

from fastapi import Depends

from src.allocations.adapters.uow import BatchAllocationsUnitOfWork
from src.allocations.services.allocation_service import AllocationService


def get_unit_of_work() -> BatchAllocationsUnitOfWork:
    return BatchAllocationsUnitOfWork()


def get_allocation_service(
    uof: Annotated[Any, Depends(get_unit_of_work)],
) -> AllocationService:
    return AllocationService(uow=uof)
