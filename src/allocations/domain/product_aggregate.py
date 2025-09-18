"""Implementation of Optimistic Concurrency Control (OCC) / Optimistic Locking."""

from typing import Set, List, Optional

from sqlalchemy.orm import reconstructor

from src.allocations.domain import batch as domain
from src.allocations.domain import events
from src.orders.domain.order_line_model import OrderLineModel


class ProductAggregate:
    """Aggregate root"""

    sku: str
    version_number: int
    batches: Set[domain.BatchModel]
    events: List[events.Event]

    def __init__(
        self, sku: str, batches: Set[domain.BatchModel], version_number: int = 0
    ):
        self.sku = sku
        self.version_number = version_number
        self._batches = batches
        self.events = []

    @reconstructor
    def init_on_load(self):
        """Called by SQLAlchemy after loading from DB"""
        self.events = []

    def allocate(self, line: OrderLineModel) -> Optional[str]:
        try:
            batch = next(b for b in sorted(self._batches) if b.can_allocate(line))
            batch.allocate(line)
            return batch.reference
        except StopIteration:
            self.events.append(events.OutOfStockEvent(sku=line.sku))
            return None
