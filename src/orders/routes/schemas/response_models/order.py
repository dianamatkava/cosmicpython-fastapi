from typing import Annotated

from pydantic import Field

from src.orders.adapters.orm import OrderStatus
from src.orders.routes.schemas.shared import BaseResponseModel


class OrderCreateResponseModel(BaseResponseModel):
    id: Annotated[int, Field(description="Order ID")]
    status: Annotated[OrderStatus, Field(description="Order status")]


class OrderResponseModel(BaseResponseModel):
    id: Annotated[int, Field(description="ID")]
    order_id: Annotated[int, Field(description="Order ID")]
    order_status: Annotated[OrderStatus, Field(description="Order status")]
    order_line_id: Annotated[int, Field(description="Order Line ID")]
    product_sku: Annotated[int, Field(description="Product SKU")]
    product_qty: Annotated[int, Field(description="Purchased product quantity")]
