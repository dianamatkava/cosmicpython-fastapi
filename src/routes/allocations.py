from typing import Annotated, Any

from fastapi import APIRouter
from fastapi import Depends, Body
from starlette import status

from src.conf import get_batch_service

router = APIRouter(prefix="/allocations")



@router.get(
"",
    status_code=status.HTTP_200_OK,
    responses={400: {"model": OutOfStockResponseModel}}
)
def home(body: Body(AllocationsAllocateIn), batch_service: Annotated[Any, Depends(get_batch_service)]):
    batch_service.allocate(body)


@router.post(
"",
    status_code=status.HTTP_200_OK,
    responses={400: {"model": OutOfStockResponseModel}}
)
def home(body: Body(AllocationsAllocateIn), batch_service: Annotated[Any, Depends(get_batch_service)]):
    batch_service.allocate(body)


@router.delete("", status_code=status.HTTP_200_OK)
def home(body: Body(AllocationsDeallocateIn), batch_service: Annotated[Any, Depends(get_batch_service)]):
    batch_service.deallocate(body)
