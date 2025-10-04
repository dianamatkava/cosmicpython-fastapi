from typing import Annotated, Optional

from pydantic import Field

from src.orders.services.schemas.order_line_dto import OrderLineSchemaDTO


class OrderLineResponseModel(OrderLineSchemaDTO):
    id: Annotated[Optional[int], Field(description="Order Line ID")] = None
    order_id: Annotated[int, Field(description="Order unique ID.")]
    sku: Annotated[str, Field(description="SKU (Stock Keeping Unit) of the product.")]
    qty: Annotated[int, Field(description="Quantity of the product.")]
