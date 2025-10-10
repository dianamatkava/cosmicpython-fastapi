from typing import Annotated, Optional

from pydantic import Field

from src.orders.services.schemas.order_line_dto import OrderLineSchemaDTO


class OrderLineCreateRequestModel(OrderLineSchemaDTO):
    """Order line create request model."""

    id: Annotated[None, Field(None, exclude=True)]
    order_id: Annotated[
        Optional[int],
        Field(description="Associated order unique ID. Null if first order item."),
    ] = None
    sku: Annotated[
        str,
        Field(..., description="SKU (Stock Keeping Unit) of the product to allocate."),
    ]
    qty: Annotated[
        int, Field(..., ge=1, description="Quantity of the product to allocate.")
    ]
