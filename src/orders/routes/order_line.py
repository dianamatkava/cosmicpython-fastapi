from typing import Annotated

from fastapi import APIRouter, Path, Depends
from starlette import status

from src.orders.conf import get_order_line_service
from src.orders.routes.schemas.response_models import OrderLineResponseModel
from src.orders.services.order_line_service import OrderLineService

router = APIRouter(prefix="/order_line", tags=["order_line"])


@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderLineResponseModel)
def get_order_lines(
    order_id: Annotated[str, Path(..., description="Identifier of the order.")],
    order_line_service: Annotated[OrderLineService, Depends(get_order_line_service)]
) -> OrderLineResponseModel:
    return order_line_service.get_order_line(order_id=order_id)


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
