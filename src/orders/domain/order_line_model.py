"""Contains 'pure' business logic models."""

from dataclasses import dataclass
from typing import Optional


@dataclass(unsafe_hash=True)
class OrderLineModel:
    id: int
    order_id: int
    sku: str
    qty: int

    def __str__(self):
        return f"{self.qty} units of {self.sku}"

    def __init__(self, order_id: int, sku: str, qty: int, id: Optional[int] = None):
        if qty <= 0:
            raise ValueError  # TODO: raise proper error

        self.id = id
        self.order_id = order_id
        self.sku = sku
        self.qty = qty
