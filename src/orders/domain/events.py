from src.constants import Queues
from src.orders.adapters.orm import OrderStatus
from src.shared.domain.events import Event


class OrderCreated(Event):
    _routing_key = Queues.ORDER_CREATED_EVENT
    _aggregate_type = "OrderCreated"
    order_id: int
    order_status: OrderStatus


class OrderLineAdded(Event):
    _routing_key = Queues.ORDER_LINE_ADDED_EVENT
    _aggregate_type = "OrderCreated"
    order_id: int
    order_line_id: int
    product_sku: str
    product_qty: int


class OrderLineRemoved(Event):
    _routing_key = Queues.ORDER_LINE_REMOVED_EVENT
    _aggregate_type = "OrderCreated"
    order_id: int
    order_line_id: int


class OrderStatusChanged(Event):
    _routing_key = Queues.ORDER_STATUS_CHANGE_EVENT
    _aggregate_type = "OrderCreated"
    order_id: int
    order_status: OrderStatus


class OrderPayed(Event):
    _routing_key = Queues.ORDER_PAYED_EVENT
    _aggregate_type = "OrderCreated"
    order_id: int


class OrderShipped(Event):
    _routing_key = Queues.ORDER_SHIPPED_EVENT
    _aggregate_type = "OrderCreated"
    order_id: int
