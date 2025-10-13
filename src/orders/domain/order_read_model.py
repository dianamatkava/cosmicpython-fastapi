from dataclasses import dataclass

from src.orders.adapters.orm import OrderStatus


@dataclass(unsafe_hash=True)
class OrderReadModel:
    order_id: int
    order_status: OrderStatus
    order_line_id: int
    product_sku: str
    product_qty: int

    def __init__(
        self,
        order_id: int,
        order_status: OrderStatus,
        order_line_id: int,
        product_sku: str,
        product_qty: int,
    ):
        self.order_id = order_id
        self.order_status = order_status
        self.order_line_id = order_line_id
        self.product_sku = product_sku
        self.product_qty = product_qty
