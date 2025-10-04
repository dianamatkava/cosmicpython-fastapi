from src.orders.domain.order_model import OrderModel
from src.orders.services.schemas.order_dto import OrderSchemaDTO


def transform_order_dto_to_domain(order: OrderSchemaDTO) -> OrderModel:
    return OrderModel(id=order.id)


def transform_order_domain_to_dto(order: OrderModel) -> OrderSchemaDTO:
    return OrderSchemaDTO(id=order.id, status=order.status)
