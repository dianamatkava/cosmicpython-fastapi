"""business logic, Accepts only primitives or a minimal DTO"""

import uuid
from typing import List

from sqlalchemy.exc import NoResultFound

from src.orders.adapters.uow import OrderLineUnitOfWork
from src.orders.domain.order_line_model import OrderLineModel
from src.orders.services.schemas.order_line_dto import OrderLineSchemaDTO
from src.orders.services.transformers.order_line_transformers import (
    transform_order_line_domain_to_dto,
)


class OrderLineService:
    uow: OrderLineUnitOfWork

    def __init__(self, uow: OrderLineUnitOfWork):
        self.uow = uow

    def create_order_line(self, sku: str, qty: int) -> OrderLineSchemaDTO:
        order_id = str(uuid.uuid4())
        with self.uow as uow:
            # TODO: FK on sku
            try:
                uow.product_repo.get(sku)
            except NoResultFound:
                # TODO: proper exception handling
                raise
            uow.order_line_repo.add(OrderLineModel(order_id, sku, qty))
            order_line = uow.order_line_repo.get(order_id=order_id)
            uow.commit()
        return transform_order_line_domain_to_dto(order_line)

    def get_order_line(self, order_id: str) -> OrderLineSchemaDTO:
        with self.uow as uow:
            return transform_order_line_domain_to_dto(uow.order_line_repo.get(order_id))

    def get_all_order_lines(self) -> List[OrderLineSchemaDTO]:
        with self.uow as uow:
            return [
                transform_order_line_domain_to_dto(order_line)
                for order_line in uow.order_line_repo.list()
            ]

    def delete_order_line(self, order_id: str) -> None:
        with self.uow as uow:
            uow.order_line_repo.delete(order_id=order_id)
            uow.commit()
