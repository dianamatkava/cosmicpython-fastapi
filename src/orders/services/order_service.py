"""Business logic, Accepts only primitives or a minimal DTO"""

from typing import List

from sqlalchemy.exc import NoResultFound

from src.orders.adapters.uow import OrderUnitOfWork
from src.orders.domain.order_model import OrderModel
from src.orders.services.schemas.order_dto import OrderSchemaDTO
from src.orders.services.schemas.order_line_dto import OrderLineSchemaDTO
from src.orders.services.transformers.order_line_transformers import (
    transform_order_line_dto_to_domain,
    transform_order_line_domain_to_dto,
)
from src.orders.services.transformers.order_transformers import (
    transform_order_read_model_to_dto,
)


class OrderService:
    uow: OrderUnitOfWork

    def __init__(self, uow: OrderUnitOfWork):
        self.uow = uow

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

    def create_order_line(self, order_line: OrderLineSchemaDTO) -> OrderLineSchemaDTO:
        with self.uow as uow:
            try:
                uow.product_repo.get(sku=order_line.sku)
            except NoResultFound:
                # TODO: AT-115 proper exception handling
                raise

            if order_line.order_id is None:
                order = OrderModel()
                uow.order_repo.add(order)
                uow.flush()
                order_line.order_id = order.id

            # TODO: AT-115 check if not similar items
            order_line_model = transform_order_line_dto_to_domain(order_line)
            uow.order_line_repo.add(order_line_model)
            uow.commit()
        return transform_order_line_domain_to_dto(order_line_model)

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
