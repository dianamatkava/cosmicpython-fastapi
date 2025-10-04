from dataclasses import dataclass
from typing import Optional

from src.orders.adapters.orm import OrderStatus


@dataclass(unsafe_hash=True)
class OrderModel:
    id: int
    status: OrderStatus

    def __init__(self, id: Optional[int] = None):
        self.id = id
