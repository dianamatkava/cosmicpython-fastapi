from typing import Annotated, Any

from fastapi import APIRouter
from fastapi import Depends, Body
from starlette import status

from src.conf import get_batch_service
from src.routes.schemas.allocations import AllocationsAllocateIn, AllocationsDeallocateIn, AllocationsOut, \
    AllocationsAllocateOut

router = APIRouter(prefix="/batch")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
def get_batches(
    batch_service: Annotated[Any, Depends(get_batch_service)]
):
    raise NotImplementedError


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def add_batch(
    body: Annotated[AllocationsAllocateIn, Body(...)],
    batch_service: Annotated[Any, Depends(get_batch_service)]
) -> None:
    batch_service.add_batch(body)


@router.delete(
    "",
    status_code=status.HTTP_200_OK,
)
def delete_batch(
    batch_service: Annotated[Any, Depends(get_batch_service)]
):
    raise NotImplementedError
