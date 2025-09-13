from typing import Annotated, ClassVar

from pydantic import Field

from src.orders.services.schemas.order_line_dto import OrderLineSchemaDTO


class OrderLineCreateRequestModel(OrderLineSchemaDTO):
    """Order line create request model."""

    id: ClassVar[None] = None
    order_id: Annotated[str, Field(description="Associated order unique ID.")]
    sku: Annotated[
        str,
        Field(..., description="SKU (Stock Keeping Unit) of the product to allocate."),
    ]
    qty: Annotated[
        int, Field(..., ge=1, description="Quantity of the product to allocate.")
    ]
