from typing import Annotated

from fastapi import APIRouter, Depends, Body, Path
from starlette import status

from src.allocations.adapters.uow import ProductAggregateUnitOfWork
from src.allocations.conf import get_allocation_service, get_unit_of_work
from src.allocations.domain.events import AllocationRequired
from src.allocations.routes.schemas.allocations.request_models import (
    AllocationRequestModel,
)
from src.allocations.routes.schemas.allocations.response_models import (
    AllocationsAllocateResponseModel,
)
from src.allocations.services.allocation_service import AllocationService
from src.allocations.services.messagebus import handle

router = APIRouter(prefix="/allocations", tags=["allocations"])
# TODO: Internal Auth


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=AllocationsAllocateResponseModel,
)
def allocate_order_line(
    body: Annotated[
        AllocationRequestModel,
        Body(..., description="The order line details to allocate"),
    ],
    uow: Annotated[ProductAggregateUnitOfWork, Depends(get_unit_of_work)],
) -> AllocationsAllocateResponseModel:
    """
    Allocates an order line to the most suitable batch.
    Will raise an error if no suitable batch is found or if the requested quantity
    cannot be satisfied by available batches.
    """
    ref, order_id = handle(uow, AllocationRequired(order_line_id=body.order_line_id))
    return AllocationsAllocateResponseModel(reference=ref, order_id=order_id)


@router.delete(
    "/{order_line_id}/batch/{ref}", status_code=status.HTTP_200_OK, response_model=None
)
def deallocate_order_line(
    order_line_id: Annotated[
        int, Path(..., description="The ID of the order line to deallocate")
    ],
    ref: Annotated[
        str, Path(..., description="The reference of the batch to deallocate")
    ],
    allocation_service: Annotated[AllocationService, Depends(get_allocation_service)],
) -> None:
    """
    Removes an order line allocation from a specific batch.
    Will return 404 if either the order or batch is not found.
    The freed quantity becomes available for future allocations.
    """
    allocation_service.deallocate(order_line_id=order_line_id, ref=ref)
