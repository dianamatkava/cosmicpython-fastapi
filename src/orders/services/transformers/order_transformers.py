from src.orders.domain.order_model import OrderModel
from src.orders.domain.order_read_model import OrderReadModel
from src.orders.services.schemas.order_dto import OrderCreateSchemaDTO, OrderSchemaDTO


def transform_order_domain_to_create_dto(order: OrderModel) -> OrderCreateSchemaDTO:
    return OrderCreateSchemaDTO(id=order.id, status=order.status)


def transform_order_read_model_to_dto(order: OrderReadModel) -> OrderSchemaDTO:
    return OrderSchemaDTO(
        order_id=order.order_id,
        order_status=order.order_status,
        order_line_id=order.order_line_id,
        product_sku=order.product_sku,
        product_qty=order.product_qty,
    )
