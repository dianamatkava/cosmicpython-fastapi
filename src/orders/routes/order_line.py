from typing import Annotated

from fastapi import APIRouter, Path
from starlette import status

router = APIRouter(prefix="/allocations", tags=["allocations"])


@router.get("/{order_id}", status_code=status.HTTP_200_OK)
def get_order_lines(
    order_id: Annotated[str, Path(..., description="Identifier of the order.")],
):
    raise NotImplementedError


@router.get("", status_code=status.HTTP_200_OK)
def list_order_lines():
    raise NotImplementedError


@router.post("", status_code=status.HTTP_201_CREATED)
def create_order_line():
    raise NotImplementedError


@router.put("", status_code=status.HTTP_200_OK)
def update_order_line():
    raise NotImplementedError


@router.delete("", status_code=status.HTTP_200_OK)
def delete_order_line():
    raise NotImplementedError
