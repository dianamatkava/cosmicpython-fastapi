from src.adapters import email
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
from src.service_manager import service_manager


def order_line_created_event_db(uow: OrderUnitOfWork, event: OrderLineAdded):
    with uow as uow:
        read_model = OrderReadModel(
            order_id=event.order_id,
            order_status=event.order_status,
            order_line_id=event.order_line_id,
            product_sku=event.product_sku,
            product_qty=event.product_qty,
        )
        uow.session.add(read_model)
        uow.commit()
        print(f"Order Line saved to DB {event.order_line_id}")


def order_line_created_event_mem(event: OrderLineAdded, *args, **kwargs):
    client = service_manager.get_mem_storage_client()
    client.create_document(
        name=f"order:{event.order_id}", data=event.model_dump(mode="json")
    )
    print(f"Order Line saved in mem {event.order_line_id}")


def order_created_event_email(event: OrderCreated, *args, **kwargs):
    email.send_mail(f"Order Created order_id={event.order_id}")


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
    with uow as uow:
        uow.order_view_repo.update(
            order_id=event.order_id,
            order_line_id=event.order_line_id,
            product_sku=event.product_sku,
            product_qty=event.product_qty,
        )
        uow.commit()


def order_status_changed_notify_event(event: OrderStatusChanged, *args, **kwargs):
    email.send_mail(f"Order Status Changed order_id={event.order_id}")


def order_payed_notify_event(event: OrderPayed, *args, **kwargs):
    email.send_mail(f"Order Payed order_id={event.order_id}")


def order_shipped_notify_event(event: OrderShipped, *args, **kwargs):
    email.send_mail(f"Order Shipped order_id={event.order_id}")
