from typing import Set

from src.allocations.domain.batch_domain_model import BatchModel
from src.allocations.services.allocation_service import OutOfStock
from src.orders.domain.order_line_model import OrderLineModel


class ProductAggregate:
    sku: str
    version_number: int
    batches: Set[BatchModel]

    def __init__(self, sku):
        self.sku = sku

    def allocate(self, order_line: OrderLineModel) -> str:
        try:
            batch = next(
                b for b in sorted(self.batches) if b.can_deallocate(order_line)
            )
            batch.allocate(order_line)
            return batch.reference
        except StopIteration:
            raise OutOfStock(f"Out of stock for sku {order_line.sku}")
