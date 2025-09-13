from typing import Annotated

from pydantic import Field

from src.orders.services.schemas.order_line_dto import OrderLineSchemaDTO


class OrderLineResponseModel(OrderLineSchemaDTO):
    order_id: Annotated[str, Field(description="Order unique ID.")]
    sku: Annotated[str, Field(description="SKU (Stock Keeping Unit) of the product.")]
    qty: Annotated[int, Field(description="Quantity of the product.")]
