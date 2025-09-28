from typing import Annotated

from fastapi import APIRouter, Depends, Body, Path
from starlette import status

from adapters.rabbitmqclient import MessagingClient
from src.inventory.conf import get_messaging_client
from src.inventory.domain.commands import AllocateOrderLine, DeallocateOrderLine
from src.inventory.routes.schemas.request_models.allocations import (
    AllocationRequestModel,
)

router = APIRouter(prefix="/allocations", tags=["allocations"])
# TODO: Internal Auth


@router.post(
    "",
    status_code=status.HTTP_202_ACCEPTED
)
def allocate_order_line(
    body: Annotated[
        AllocationRequestModel,
        Body(..., description="The order line details to allocate"),
    ],
    messaging_client: Annotated[MessagingClient, Depends(get_messaging_client)]
) -> None:
    """
    Allocates an order line to the most suitable batch.
    Will raise an error if no suitable batch is found or if the requested quantity
    cannot be satisfied by available batches.
    """
    cmd = AllocateOrderLine(order_line_id=body.order_line_id)
    messaging_client.publish('allocate', cmd.model_dump_json())


@router.delete(
    "/batch/{ref}/{order_line_id}", status_code=status.HTTP_202_ACCEPTED
)
def deallocate_order_line(
    order_line_id: Annotated[
        int, Path(..., description="The ID of the order line to deallocate")
    ],
    ref: Annotated[
        str, Path(..., description="The reference of the batch to deallocate")
    ],
    messaging_client: Annotated[MessagingClient, Depends(get_messaging_client)],
) -> None:
    """
    Removes an order line allocation from a specific batch.
    Will return 404 if either the order or batch is not found.
    The freed quantity becomes available for future inventory.
    """
    cmd = DeallocateOrderLine(order_line_id=order_line_id, ref=ref)
    messaging_client.publish('deallocate', cmd.model_dump_json())

