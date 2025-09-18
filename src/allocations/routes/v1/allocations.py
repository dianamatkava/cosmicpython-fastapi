from typing import Annotated

from fastapi import APIRouter, Depends, Body, Path
from starlette import status

from src.allocations.conf import get_allocation_service
from src.allocations.routes.schemas.allocations.request_models import (
    AllocationRequestModel,
)
from src.allocations.routes.schemas.allocations.response_models import (
    AllocationsAllocateResponseModel,
)
from src.allocations.services.allocation_service import AllocationService

router = APIRouter(prefix="/v1/allocations", tags=["allocations"])
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
    allocation_service: Annotated[AllocationService, Depends(get_allocation_service)],
) -> AllocationsAllocateResponseModel:
    """
    Allocates an order line to the most suitable batch.
    Will raise an error if no suitable batch is found or if the requested quantity
    cannot be satisfied by available batches.
    """
    ref, order_id = allocation_service.allocate(body.order_line_id)
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
