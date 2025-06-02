"""Contains 'pure' business logic models."""

from dataclasses import dataclass
from datetime import date
from typing import Set, Optional


@dataclass(unsafe_hash=True)
class OrderLineModel:
    order_id: str
    sku: str
    qty: int

    def __str__(self):
        return f"{self.qty} units of {self.sku}"


class BatchModel:
    reference: str
    sku: str
    eta: date | None
    _purchased_quantity: int  # initial quantity
    _allocations: Set[OrderLineModel]

    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()

    def __str__(self):
        return f"{self.available_quantity} {self.sku}"

    # Batch is entity object
    # Entity described by ref
    # batch entity is not described by its values, likewise value object
    def __eq__(self, other):
        if not isinstance(other, BatchModel):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other: "BatchModel") -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    @property
    def allocations(self) -> set[OrderLineModel]:
        return self._allocations

    @property
    def allocated_quantity(self) -> int:
        return sum([allocation.qty for allocation in self._allocations])

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def allocate(self, order_line: OrderLineModel):
        if self.can_allocate(order_line):
            self._allocations.add(order_line)

    def can_allocate(self, order_line: OrderLineModel) -> bool:
        if self.sku == order_line.sku and self.available_quantity >= order_line.qty:
            return True
        return False

    def deallocate(self, order_line: OrderLineModel):
        if self.can_deallocate(order_line):
            self._allocations.remove(order_line)

    def can_deallocate(self, order_line: OrderLineModel) -> bool:
        if order_line in self._allocations:
            return True
        return False
