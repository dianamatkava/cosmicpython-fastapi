"""Business logic, Accepts only primitives or a minimal DTO"""

from typing import List

from src.orders.adapters.uow.order_uow import OrderUnitOfWork
from src.orders.domain.order_model import OrderModel
from src.orders.services.schemas.order_dto import OrderCreateSchemaDTO, OrderSchemaDTO
from src.orders.services.transformers.order_transformers import (
    transform_order_domain_to_create_dto,
    transform_order_read_model_to_dto,
)


class OrderService:
    uow: OrderUnitOfWork

    def __init__(self, uow: OrderUnitOfWork):
        self.uow = uow

    def create_order(self) -> OrderCreateSchemaDTO:
        with self.uow as uow:
            order_model = OrderModel()
            uow.order_repo.add(order_model)
            # CQSP post Read model update
            uow.flush()
            order_model.created()
            uow.commit()
        return transform_order_domain_to_create_dto(order_model)

    def get_order(self, order_id: int) -> OrderSchemaDTO:
        with self.uow as uow:
            return transform_order_read_model_to_dto(uow.order_view_repo.get(order_id))

    def get_all_orders(self) -> List[OrderSchemaDTO]:
        with self.uow as uow:
            return [
                transform_order_read_model_to_dto(order_line)
                for order_line in uow.order_view_repo.list()
            ]

    def delete_order(self, order_id: int) -> None:
        raise NotImplementedError
