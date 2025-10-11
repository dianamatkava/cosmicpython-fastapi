from typing import Optional

from pydantic import BaseModel

from src.orders.adapters.orm import OrderStatus


class OrderCreateSchemaDTO(BaseModel):
    id: Optional[int] = None
    status: OrderStatus = None


class OrderSchemaDTO(BaseModel):
    order_id: int
    order_status: OrderStatus
    order_line_id: int
    product_sku: str
    product_qty: int
