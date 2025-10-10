from typing import Annotated, List

from fastapi import APIRouter, Path, Depends
from pydantic import TypeAdapter
from starlette import status

from src.orders.conf import get_order_service
from src.orders.routes.schemas.response_models.order import (
    OrderResponseModel,
)
from src.orders.services.order_service import OrderService

router = APIRouter(prefix="/order", tags=["order"])


@router.get(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrderResponseModel,
)
def get_order_by_id(
    order_id: Annotated[int, Path(..., description="Identifier of the order.")],
    order_service: Annotated[OrderService, Depends(get_order_service)],
) -> OrderResponseModel:
    return TypeAdapter(OrderResponseModel).validate_python(
        order_service.get_order(order_id=order_id), from_attributes=True
    )


# TODO: AT-708 Add pagination
@router.get("", status_code=status.HTTP_200_OK, response_model=List[OrderResponseModel])
def list_orders(
    order_service: Annotated[OrderService, Depends(get_order_service)],
) -> List[OrderResponseModel]:
    return TypeAdapter(List[OrderResponseModel]).validate_python(
        order_service.get_all_orders(), from_attributes=True
    )


@router.delete("/{order_id}", status_code=status.HTTP_200_OK)
def delete_order(
    order_id: Annotated[str, Path(..., description="Identifier of the order line.")],
) -> None:
    raise NotImplementedError
