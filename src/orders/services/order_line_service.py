"""business logic, Accepts only primitives or a minimal DTO"""

from typing import Any, List

from src.orders.adapters.uow import OrderLineUnitOfWork
from src.orders.domain.order_line_model import OrderLineModel
from src.orders.services.schemas import OrderLineSchemaDTO


def transform_order_line_dto_to_domain(order_line: OrderLineSchemaDTO) -> OrderLineModel:
    return OrderLineModel()


class OrderLineService:
    uow: OrderLineUnitOfWork

    def __init__(self, uow: OrderLineUnitOfWork):
        self.uow = uow

    def create_order_line(self, order_line: OrderLineSchemaDTO) -> None:
        order_line_model = transform_order_line_dto_to_domain(order_line)
        with self.uow as uow:
            uow.order_line_repo.add(order_line_model)
            raise NotImplementedError

    def get_order_line(self, order_id: str) -> OrderLineSchemaDTO:
        with self.uow as uow:
            return uow.order_line_repo.get(order_id)

    def get_all_order_lines(self) -> List[OrderLineSchemaDTO]:
        with self.uow as uow:
            return uow.order_line_repo.list()

    def delete_order_line(self) -> None:
        with self.uow as uow:
            raise NotImplementedError
