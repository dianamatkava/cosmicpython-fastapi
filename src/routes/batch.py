from typing import Annotated, Any, List

from fastapi import APIRouter, Path
from fastapi import Depends, Body
from starlette import status

from src.conf import get_batch_service
from src.domain import batch_domain_model
from src.routes.exceptions.api_exceptions import OutOfStockResponseModel
from src.routes.schemas.allocations import AllocationsAllocateIn, AllocationsDeallocateIn, AllocationsOut, \
    AllocationsAllocateOut, BatchesCreationModelIn, BatchesListOut
from src.services.batch_service import OutOfStock

router = APIRouter(prefix="/batch")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
def get_batches(
    batch_service: Annotated[Any, Depends(get_batch_service)]
) -> BatchesListOut:
    return batch_service.get_batches()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def add_batch(
    body: Annotated[BatchesCreationModelIn, Body()],
    batch_service: Annotated[Any, Depends(get_batch_service)]
) -> None:
    batch_service.add_batch(ref=body.ref, sku=body.sku, qty=body.qty, eta=body.eta)


@router.delete(
    "{ref}",
    status_code=status.HTTP_200_OK,
)
def delete_batch(
    ref: Annotated[str, Path(description="")],
    batch_service: Annotated[Any, Depends(get_batch_service)]
):
    return {}
