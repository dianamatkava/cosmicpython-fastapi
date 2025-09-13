"""Contains 'pure' business logic models."""

from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class OrderLineModel:
    order_id: str
    sku: str
    qty: int

    def __str__(self):
        return f"{self.qty} units of {self.sku}"

    def __init__(self, order_id: str, sku: str, qty: int):
        if qty <= 0:
            raise ValueError  # TODO: raise proper error

        self.order_id = order_id
        self.sku = sku
        self.qty = qty
