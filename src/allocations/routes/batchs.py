from typing import Annotated

from fastapi import APIRouter, Path
from fastapi import Depends, Body
from pydantic import TypeAdapter
from starlette import status

from src.allocations.conf import get_batch_service
from src.allocations.routes.schemas.allocations.request_models import (
    BatchesCreationModelRequestModel,
)
from src.allocations.routes.schemas.allocations.response_models import (
    BatchesListResponseModel,
)
from src.allocations.services.schemas import BatchSchemaDTO
from src.allocations.services.batch_service import BatchService

router = APIRouter(prefix="/batch")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=None)
def add_batch(
    body: Annotated[BatchesCreationModelRequestModel, Body()],
    batch_service: Annotated[BatchService, Depends(get_batch_service)],
) -> None:
    batch_service.add_batch(ref=body.ref, sku=body.sku, qty=body.qty, eta=body.eta)


@router.get("", status_code=status.HTTP_200_OK, response_model=BatchesListResponseModel)
def get_batches(
    batch_service: Annotated[BatchService, Depends(get_batch_service)],
) -> BatchesListResponseModel:
    return TypeAdapter(BatchesListResponseModel).validate_python(
        batch_service.get_batches(), from_attributes=True
    )


@router.get("/{ref}", status_code=status.HTTP_200_OK, response_model=BatchSchemaDTO)
def get_batch(
    ref: Annotated[str, Path()],
    batch_service: Annotated[BatchService, Depends(get_batch_service)],
) -> BatchSchemaDTO:
    return TypeAdapter(BatchSchemaDTO).validate_python(
        batch_service.get_batche_by_ref(ref), from_attributes=True
    )


@router.delete("/{ref}", status_code=status.HTTP_200_OK, response_model=None)
def delete_batch(
    ref: Annotated[str, Path(description="")],
    batch_service: Annotated[BatchService, Depends(get_batch_service)],
) -> None:
    return batch_service.delete_batch(ref)
