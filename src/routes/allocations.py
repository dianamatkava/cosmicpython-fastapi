from typing import Annotated, Any

from fastapi import APIRouter
from fastapi import Depends, Body
from starlette import status

from src.conf import get_batch_service
from src.routes.schemas.allocations import AllocationsAllocateIn, AllocationsDeallocateIn, AllocationsOut, \
    AllocationsAllocateOut

router = APIRouter(prefix="/allocations")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=AllocationsOut
)
def home(
    body: Annotated[AllocationsAllocateIn, Body()],
    batch_service: Annotated[Any, Depends(get_batch_service)]
) -> AllocationsOut:
    return batch_service.allocate(body)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=AllocationsAllocateOut
)
def home(
    body: Annotated[AllocationsAllocateIn, Body(...)],
    batch_service: Annotated[Any, Depends(get_batch_service)]
) -> AllocationsAllocateOut:
    return AllocationsAllocateOut(batch_reference=batch_service.allocate(body))


@router.delete(
    "",
    status_code=status.HTTP_200_OK,
    response_model=AllocationsAllocateOut
)
def home(
    body: Annotated[AllocationsDeallocateIn, Body(...)],
    batch_service: Annotated[Any, Depends(get_batch_service)]
) -> AllocationsAllocateOut:
    return AllocationsAllocateOut(batch_reference=batch_service.deallocate(body))
