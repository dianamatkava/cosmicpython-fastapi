"""Implementation of Optimistic Concurrency Control (OCC) / Optimistic Locking."""

from typing import Set, List, Optional, Union

from sqlalchemy.orm import reconstructor

import src.shared.domain.events
from src.inventory.domain import batch as domain, commands
from src.inventory.domain import events
from src.orders.domain.order_line_model import OrderLineModel


class OrderLineDoesNotExists(Exception):
    pass


class ProductAggregate:
    """Product Aggregate root"""

    sku: str
    version_number: int
    batches: Set[domain.BatchModel]
    events: List[Union[src.shared.domain.events.DomainEvent, commands.Command]]

    def __init__(
        self, sku: str, batches: Set[domain.BatchModel] = None, version_number: int = 0
    ):
        self.sku = sku
        self.version_number = version_number
        self.batches = batches or set()
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
            self.events.append(
                events.OutOfStockEvent(sku=self.sku, aggregate_id=self.sku)
            )
            return None

    def deallocate(self, order_line: OrderLineModel):
        try:
            batch = next(
                b for b in sorted(self._batches) if b.can_deallocate(order_line)
            )
            batch.deallocate(order_line)
        except StopIteration:
            raise OrderLineDoesNotExists

    def change_batch_quantity(self, ref: str, qty: int):
        batch = next(b for b in sorted(self._batches) if b.reference == ref)
        batch._purchased_quantity = qty
        while batch.available_quantity < 0:
            line = batch.deallocate_one()
            self.events.append(
                commands.AllocateOrderLine(order_line_id=line.id, aggregate_id=self.sku)
            )
        self.events.append(
            events.BatchQuantityChangedEvent(ref=ref, qty=qty, aggregate_id=self.sku)
        )
