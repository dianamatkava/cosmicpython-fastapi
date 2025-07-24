from typing import Annotated

from fastapi import APIRouter, Path
from starlette import status

router = APIRouter(prefix="/allocations", tags=["allocations"])


@router.get("/{sku}", status_code=status.HTTP_200_OK)
def get_product(
    sku: Annotated[str, Path(..., description="Identifier of the product.")],
):
    raise NotImplementedError


@router.get("", status_code=status.HTTP_200_OK)
def list_product():
    raise NotImplementedError


@router.post("", status_code=status.HTTP_201_CREATED)
def create_product():
    raise NotImplementedError


@router.put("", status_code=status.HTTP_200_OK)
def update_product():
    raise NotImplementedError


@router.delete("", status_code=status.HTTP_200_OK)
def delete_product():
    raise NotImplementedError
