from typing import Annotated, List

from fastapi import APIRouter, Path, Depends, Body
from pydantic import TypeAdapter
from starlette import status

from src.orders.conf import get_order_service
from src.orders.routes.schemas.request_models.order_line import (
    OrderLineCreateRequestModel,
)
from src.orders.routes.schemas.response_models.order_line import OrderLineResponseModel
from src.orders.services.order_service import OrderService

router = APIRouter(prefix="/order_line", tags=["order_line"])
# TODO: Client Auth


@router.get(
    "/{order_line_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrderLineResponseModel,
)
def get_order_line_by_id(
    order_line_id: Annotated[int, Path(..., description="Identifier of the order.")],
    order_service: Annotated[OrderService, Depends(get_order_service)],
) -> OrderLineResponseModel:
    return TypeAdapter(OrderLineResponseModel).validate_python(
        order_service.get_order_line(id=order_line_id), from_attributes=True
    )


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=List[OrderLineResponseModel]
)
def list_order_lines(
    order_service: Annotated[OrderService, Depends(get_order_service)],
) -> List[OrderLineResponseModel]:
    return TypeAdapter(List[OrderLineResponseModel]).validate_python(
        order_service.get_all_order_lines(), from_attributes=True
    )


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=OrderLineResponseModel
)
def create_order_line(
    order_service: Annotated[OrderService, Depends(get_order_service)],
    body: Annotated[
        OrderLineCreateRequestModel,
        Body(..., description="The order line details to create"),
    ],
) -> OrderLineResponseModel:
    return TypeAdapter(OrderLineResponseModel).validate_python(
        order_service.create_order_line(body),
        from_attributes=True,
    )


@router.delete("/{order_line_id}", status_code=status.HTTP_200_OK)
def delete_order_line(
    order_line_id: Annotated[
        int, Path(..., description="Identifier of the order line.")
    ],
    order_service: Annotated[OrderService, Depends(get_order_service)],
) -> None:
    order_service.delete_order_line(id=order_line_id)
