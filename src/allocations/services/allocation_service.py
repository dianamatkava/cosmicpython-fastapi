"""business logic, Accepts only primitives or a minimal DTO"""

from typing import Tuple

from src.allocations.adapters.uow import ProductAggregateUnitOfWork
from src.allocations.domain.product_agregate_model import ProductAggregate
from src.allocations.services import messagebus


class OutOfStock(Exception):
    """OutOfStock Exception"""


class AllocationService:
    uow: ProductAggregateUnitOfWork

    def __init__(self, uow: ProductAggregateUnitOfWork):
        self.uow = uow

    def allocate(self, order_line_id: int) -> Tuple[str, str]:
        with self.uow as uow:
            order_line = uow.order_line_repo.get(id=order_line_id)
            product: ProductAggregate = uow.product_aggregate_repo.get(
                sku=order_line.sku
            )
            batch_ref: str = product.allocate(order_line)
            messagebus.dispatch(product.events)
            if not batch_ref:
                raise OutOfStock()
            # OCC check with CAS
            uow.product_aggregate_repo.cas(product)
            uow.commit()
        return batch_ref, order_line.order_id

    def deallocate(self, order_line_id: int, ref: str) -> None:
        with self.uow as uow:
            order_line = uow.order_line_repo.get(id=order_line_id)
            product = uow.product_aggregate_repo.get(sku=order_line.sku)
            product.deallocate(order_line)
            uow.commit()
