from typing import Annotated

from fastapi import APIRouter, Depends, Body, Path
from starlette import status

from src.inventory.adapters.uow import ProductAggregateUnitOfWork
from src.inventory.conf import get_unit_of_work
from src.inventory.domain.events import (
    AllocationRequiredEvent,
    BatchQuantityChangedEvent,
    DeallocateOrderLineEvent,
)
from src.inventory.routes.schemas.request_models.allocations import (
    AllocationRequestModel,
    ChangeBatchQuantityRequestModel,
)
from src.inventory.routes.schemas.response_models.allocations import (
    AllocationsAllocateResponseModel,
)
from src.inventory.services.messagebus import handle

router = APIRouter(prefix="/v2/inventory", tags=["inventory"])
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
    ref, order_id, *_ = handle(
        uow, AllocationRequiredEvent(order_line_id=body.order_line_id)
    )
    return AllocationsAllocateResponseModel(reference=ref, order_id=order_id)


@router.delete(
    "/batch/{ref}/{order_line_id}", status_code=status.HTTP_200_OK, response_model=None
)
def deallocate_order_line(
    order_line_id: Annotated[
        int, Path(..., description="The ID of the order line to deallocate")
    ],
    ref: Annotated[
        str, Path(..., description="The reference of the batch to deallocate")
    ],
    uow: Annotated[ProductAggregateUnitOfWork, Depends(get_unit_of_work)],
) -> None:
    """
    Removes an order line allocation from a specific batch.
    Will return 404 if either the order or batch is not found.
    The freed quantity becomes available for future inventory.
    """
    handle(uow, DeallocateOrderLineEvent(order_line_id=order_line_id, ref=ref))


@router.put("/batch/{ref}", status_code=status.HTTP_200_OK, response_model=None)
def update_batch(
    body: Annotated[
        ChangeBatchQuantityRequestModel,
        Body(..., description="Batch update body schema"),
    ],
    ref: Annotated[
        str, Path(..., description="The reference of the batch to deallocate")
    ],
    uow: Annotated[ProductAggregateUnitOfWork, Depends(get_unit_of_work)],
) -> None:
    if isinstance(body, ChangeBatchQuantityRequestModel):
        handle(uow, BatchQuantityChangedEvent(ref=ref, qty=body.qty))
    else:
        raise NotImplementedError
