"""Implementation of Optimistic Concurrency Control (OCC) / Optimistic Locking."""

from typing import Set

from src.allocations.domain.batch_domain_model import BatchModel
from src.orders.domain.order_line_model import OrderLineModel


class ProductAggregate:
    """Aggregate root"""

    sku: str
    version_number: int
    batches: Set[BatchModel]

    def __init__(self, sku: str, batches: Set[BatchModel], version_number: int = 0):
        self.sku = sku
        self.version_number = version_number
        self._batches = batches

    def allocate(self, line: OrderLineModel) -> str:
        try:
            batch = next(b for b in sorted(self._batches) if b.can_allocate(line))
            batch.allocate(line)
            return batch.reference
        except StopIteration:
            raise ValueError(f"Out of stock for sku {line.sku}")
