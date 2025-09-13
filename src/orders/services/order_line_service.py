"""business logic, Accepts only primitives or a minimal DTO"""

from typing import List

from sqlalchemy.exc import NoResultFound

from src.orders.adapters.uow import OrderLineUnitOfWork
from src.orders.services.schemas.order_line_dto import OrderLineSchemaDTO
from src.orders.services.transformers.order_line_transformers import (
    transform_order_line_domain_to_dto,
    transform_order_line_dto_to_domain,
)


class OrderLineService:
    uow: OrderLineUnitOfWork

    def __init__(self, uow: OrderLineUnitOfWork):
        self.uow = uow

    def create_order_line(self, order_line: OrderLineSchemaDTO) -> OrderLineSchemaDTO:
        with self.uow as uow:
            # TODO: FK on sku and order
            try:
                uow.product_repo.get(order_line.sku)
            except NoResultFound:
                # TODO: proper exception handling
                raise
            # TODO: check if not similar items
            order_line_model = transform_order_line_dto_to_domain(order_line)
            uow.order_line_repo.add(order_line_model)
            uow.commit()
        return transform_order_line_domain_to_dto(order_line_model)

    # TODO: add update

    def get_order_line(self, id: int) -> OrderLineSchemaDTO:
        with self.uow as uow:
            return transform_order_line_domain_to_dto(uow.order_line_repo.get(id))

    def get_all_order_lines(self) -> List[OrderLineSchemaDTO]:
        with self.uow as uow:
            return [
                transform_order_line_domain_to_dto(order_line)
                for order_line in uow.order_line_repo.list()
            ]

    def delete_order_line(self, id: int) -> None:
        with self.uow as uow:
            uow.order_line_repo.delete(id=id)
            uow.commit()
