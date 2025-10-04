from typing import Annotated

from pydantic import Field

from src.orders.services.schemas.order_line_dto import OrderLineSchemaDTO


class OrderLineCreateRequestModel(OrderLineSchemaDTO):
    """Order line create request model."""

    order_id: Annotated[int, Field(description="Associated order unique ID.")]
    sku: Annotated[
        str,
        Field(..., description="SKU (Stock Keeping Unit) of the product to allocate."),
    ]
    qty: Annotated[
        int, Field(..., ge=1, description="Quantity of the product to allocate.")
    ]
