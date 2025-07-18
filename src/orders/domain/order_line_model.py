"""Contains 'pure' business logic models."""

from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class OrderLineModel:
    order_id: str
    sku: str
    qty: int

    def __str__(self):
        return f"{self.qty} units of {self.sku}"
