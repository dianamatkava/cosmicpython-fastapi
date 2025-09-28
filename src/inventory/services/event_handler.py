"""Event-Driven API handlers"""

from typing import Tuple

from src.adapters import email
from src.inventory.adapters.uow import ProductAggregateUnitOfWork
from src.inventory.domain import events, commands
from src.inventory.domain.product_aggregate import ProductAggregate


class OutOfStock(Exception):
    pass


def allocate(
    uow: ProductAggregateUnitOfWork, event: commands.AllocateOrderLine
) -> Tuple[str, int]:
    print(f"Allocate Started event: {event}")
    with uow as uow:
        order_line = uow.order_line_repo.get(id=event.order_line_id)
        product: ProductAggregate = uow.product_aggregate_repo.get(sku=order_line.sku)
        batch_ref: str = product.allocate(order_line)
        if not batch_ref:
            raise OutOfStock()
        # OCC check with CAS
        uow.product_aggregate_repo.cas(product)
        uow.commit()
    return batch_ref, order_line.order_id


def deallocate(uow: ProductAggregateUnitOfWork, order_line_id: int, ref: str) -> None:
    print(f"Deallocate Started event: {order_line_id}")
    with uow as uow:
        order_line = uow.order_line_repo.get(id=order_line_id)
        product = uow.product_aggregate_repo.get(sku=order_line.sku)
        product.deallocate(order_line)
        uow.commit()


def change_batch_quantity(
    uow: ProductAggregateUnitOfWork, event: commands.ChangeBatchQuantity
):
    print(f"change_batch_quantity event: {event}")
    with uow as uow:
        product: ProductAggregate = uow.product_aggregate_repo.get(ref=event.ref)
        product.change_batch_quantity(ref=event.ref, qty=event.qty)
        uow.commit()
        return product


def send_out_of_stock_event(
    uow: ProductAggregateUnitOfWork, event: events.OutOfStockEvent
):
    print(f"send_out_of_stock_event event: {event}")
    # signal purchasing team to issue more batches
    print(f"{event}")
    email.send_mail(event.sku)


def batch_quantity_changed_event(
    uow: ProductAggregateUnitOfWork, event: events.BatchQuantityChangedEvent
):
    print(f"batch_quantity_changed_event event: {event}")
    # signal purchasing team to issue more batches
    print(f"{event}")
    email.send_mail(event.ref)
