from typing import Annotated, Any

from fastapi import APIRouter
from fastapi import Depends, Body
from starlette import status

from src.conf import get_batch_service
from src.routes.exceptions.api_exceptions import OutOfStockResponseModel
from src.routes.models.allocations import AllocationsAllocateIn, AllocationsDeallocateIn, AllocationsOut, \
    AllocationsAllocateOut

router = APIRouter(prefix="/allocations")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    responses={400: {"model": OutOfStockResponseModel}},
    response_model=AllocationsOut
)
def home(
    body: Body(AllocationsAllocateIn),
    batch_service: Annotated[Any, Depends(get_batch_service)]
) -> AllocationsOut:
    return batch_service.allocate(body)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": OutOfStockResponseModel}},
    response_model=AllocationsAllocateOut
)
def home(
    body: Body(AllocationsAllocateIn),
    batch_service: Annotated[Any, Depends(get_batch_service)]
) -> AllocationsAllocateOut:
    return AllocationsAllocateOut(batch_reference=batch_service.allocate(body))


@router.delete(
    "",
    status_code=status.HTTP_200_OK,
    response_model=AllocationsAllocateOut
)
def home(
    body: Body(AllocationsDeallocateIn),
    batch_service: Annotated[Any, Depends(get_batch_service)]
) -> AllocationsAllocateOut:
    return AllocationsAllocateOut(batch_reference=batch_service.deallocate(body))
