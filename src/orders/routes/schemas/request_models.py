from typing import Annotated

from pydantic import Field

from src.orders.services.schemas import OrderLineSchemaDTO


class OrderLineCreateRequestModel(OrderLineSchemaDTO):
    """Order line create request model."""

    order_id: Annotated[str, Field(description="Order unique ID.")]
    sku: Annotated[
        str, Field(description="SKU (Stock Keeping Unit) of the product to allocate.")
    ]
    qty: Annotated[int, Field(description="Quantity of the product to allocate.")]
