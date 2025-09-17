"""business logic, Accepts only primitives or a minimal DTO"""

from typing import Tuple

from src.allocations.adapters.uow import ProductAggregateUnitOfWork
from src.allocations.domain.product_aggregate import ProductAggregate
from src.allocations.services import messagebus
from src.allocations.domain import events


class OutOfStock(Exception):
    pass


def allocate(
    uow: ProductAggregateUnitOfWork, event: events.AllocationRequired
) -> Tuple[str, str]:
    with uow as uow:
        order_line = uow.order_line_repo.get(id=event.orderid)
        product: ProductAggregate = uow.product_aggregate_repo.get(sku=order_line.sku)
        batch_ref: str = product.allocate(order_line)
        messagebus.dispatch(product.events)
        if not batch_ref:
            raise OutOfStock()
        # OCC check with CAS
        uow.product_aggregate_repo.cas(product)
        uow.commit()
    return batch_ref, order_line.order_id


def deallocate(uow: ProductAggregateUnitOfWork, order_line_id: int, ref: str) -> None:
    with uow as uow:
        order_line = uow.order_line_repo.get(id=order_line_id)
        product = uow.product_aggregate_repo.get(sku=order_line.sku)
        product.deallocate(order_line)
        uow.commit()


def send_out_of_stock_event(
    uow: ProductAggregateUnitOfWork, event: events.OutOfStockEvent
):
    # signal purchasing team to issue more batches
    print(f"OutOfStockEvent sku: {event.sku}")
