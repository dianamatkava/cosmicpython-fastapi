from dataclasses import dataclass
from typing import Optional

from src.orders.adapters.orm import OrderStatus


@dataclass(unsafe_hash=True)
class OrderReadModel:
    id: int
    order_id: int
    order_status: OrderStatus
    order_line_id: int = None
    product_sku: str = None
    product_qty: int = None

    def __init__(
        self,
        order_id: int,
        order_status: OrderStatus,
        order_line_id: int = None,
        product_sku: str = None,
        product_qty: int = None,
        id: Optional[int] = None,
    ):
        self.id = id
        self.order_id = order_id
        self.order_status = order_status
        self.order_line_id = order_line_id
        self.product_sku = product_sku
        self.product_qty = product_qty
