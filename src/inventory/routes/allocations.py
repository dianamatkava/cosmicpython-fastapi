from typing import Annotated, List

from fastapi import APIRouter, Depends, Body, Path
from pydantic import TypeAdapter
from starlette import status

from src.allocations.conf import get_batch_service
from src.allocations.routes.schemas.allocations.request_models import (
    OrderLineModelRequestModel,
)
from src.allocations.routes.schemas.allocations.response_models import (
    AllocationsAllocateResponseModel,
)
from src.allocations.services.schemas import AllocationSchemaDTO
from src.allocations.services.batch_service import BatchService

router = APIRouter(prefix="/allocations", tags=["allocations"])


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=List[AllocationSchemaDTO]
)
def get_allocations(
    batch_service: Annotated[BatchService, Depends(get_batch_service)],
) -> List[AllocationSchemaDTO]:
    """
    Lists all current order line allocations in the system.
    Returns an empty list if no allocations exist.
    """
    return TypeAdapter(List[AllocationSchemaDTO]).validate_python(
        batch_service.get_allocations(), from_attributes=True
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=AllocationsAllocateResponseModel,
)
def allocate_order_line(
    body: Annotated[
        OrderLineModelRequestModel,
        Body(..., description="The order line details to allocate"),
    ],
    batch_service: Annotated[BatchService, Depends(get_batch_service)],
) -> AllocationsAllocateResponseModel:
    """
    Allocates an order line to the most suitable batch.
    Will raise an error if no suitable batch is found or if the requested quantity
    cannot be satisfied by available batches.
    """
    ref, order_id = batch_service.allocate(body)
    return AllocationsAllocateResponseModel(reference=ref, order_id=order_id)


@router.delete(
    "/{order_id}/batch/{ref}", status_code=status.HTTP_200_OK, response_model=None
)
def deallocate_order_line(
    order_id: Annotated[
        str, Path(..., description="The ID of the order to deallocate")
    ],
    ref: Annotated[
        str, Path(..., description="The reference of the batch to deallocate")
    ],
    batch_service: Annotated[BatchService, Depends(get_batch_service)],
) -> None:
    """
    Removes an order line allocation from a specific batch.
    Will return 404 if either the order or batch is not found.
    The freed quantity becomes available for future allocations.
    """
    batch_service.deallocate(order_id=order_id, batch_reference=ref)
