from src.orders.domain.order_line_model import OrderLineModel
from src.orders.services.schemas.order_line_dto import OrderLineSchemaDTO


def transform_order_line_dto_to_domain(
    order_line: OrderLineSchemaDTO,
) -> OrderLineModel:
    return OrderLineModel(
        order_id=order_line.order_id, sku=order_line.sku, qty=order_line.qty
    )


def transform_order_line_domain_to_dto(
    order_line: OrderLineModel,
) -> OrderLineSchemaDTO:
    return OrderLineSchemaDTO(
        order_id=order_line.order_id, sku=order_line.sku, qty=order_line.qty
    )
