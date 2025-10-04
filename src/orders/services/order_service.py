"""business logic, Accepts only primitives or a minimal DTO"""

from typing import List

from src.orders.adapters.uow.order_uow import OrderUnitOfWork
from src.orders.domain.order_model import OrderModel
from src.orders.services.schemas.order_dto import OrderSchemaDTO
from src.orders.services.transformers.order_transformers import (
    transform_order_domain_to_dto,
)


class OrderService:
    uow: OrderUnitOfWork

    def __init__(self, uow: OrderUnitOfWork):
        self.uow = uow

    def create_order(self) -> OrderSchemaDTO:
        with self.uow as uow:
            order_model = OrderModel()
            uow.order_repo.add(order_model)
            uow.commit()
        return transform_order_domain_to_dto(order_model)

    def get_order(self, id: int) -> OrderSchemaDTO:
        with self.uow as uow:
            return transform_order_domain_to_dto(uow.order_repo.get(id))

    def get_all_orders(self) -> List[OrderSchemaDTO]:
        with self.uow as uow:
            return [
                transform_order_domain_to_dto(order_line)
                for order_line in uow.order_repo.list()
            ]

    def delete_order(self, id: int) -> None:
        raise NotImplementedError
