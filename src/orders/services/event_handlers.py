from src.orders.adapters.uow import OrderUnitOfWork
from src.orders.domain.events import (
    OrderCreated,
    OrderShipped,
    OrderPayed,
    OrderStatusChanged,
    OrderLineRemoved,
    OrderLineAdded,
)
from src.orders.domain.order_read_model import OrderReadModel


def order_created_event(uow: OrderUnitOfWork, event: OrderCreated):
    with uow as uow:
        read_model = OrderReadModel(
            order_id=event.order_id, order_status=event.order_status
        )
        uow.order_view_repo.add(read_model)
        uow.commit()


def order_line_added_event(uow: OrderUnitOfWork, event: OrderLineAdded):
    with uow as uow:
        uow.order_view_repo.update(
            order_id=event.order_id,
            order_line_id=event.order_line_id,
            product_sku=event.product_sku,
            product_qty=event.product_qty,
        )
        uow.commit()


def order_line_removed_event(uow: OrderUnitOfWork, event: OrderLineRemoved):
    print("order_line_removed_event")


def order_status_changed_event(uow: OrderUnitOfWork, event: OrderStatusChanged):
    print("order_status_changed_event")


def order_payed_event(uow: OrderUnitOfWork, event: OrderPayed):
    print("order_payed_event")


def order_shipped_event(uow: OrderUnitOfWork, event: OrderShipped):
    print("order_shipped_event")
