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

router = APIRouter(prefix="/allocations")


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=List[AllocationSchemaDTO]
)
def get_allocations(
    batch_service: Annotated[BatchService, Depends(get_batch_service)],
) -> List[AllocationSchemaDTO]:
    return TypeAdapter(List[AllocationSchemaDTO]).validate_python(
        batch_service.get_allocations(), from_attributes=True
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=AllocationsAllocateResponseModel,
)
def allocate_order_line(
    body: Annotated[OrderLineModelRequestModel, Body(...)],
    batch_service: Annotated[BatchService, Depends(get_batch_service)],
) -> AllocationsAllocateResponseModel:
    return AllocationsAllocateResponseModel(reference=batch_service.allocate(body))


@router.delete(
    "/{order_id}/batch/{ref}", status_code=status.HTTP_200_OK, response_model=None
)
def deallocate_order_line(
    order_id: Annotated[str, Path(...)],
    ref: Annotated[str, Path(...)],
    batch_service: Annotated[BatchService, Depends(get_batch_service)],
) -> None:
    batch_service.deallocate(order_id=order_id, batch_reference=ref)
