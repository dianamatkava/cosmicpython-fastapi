"""business logic, Accepts only primitives or a minimal DTO"""

from typing import Any


class OrderLineService:
    uow: Any

    def __init__(self, uow: Any):
        self.uow = uow

    def create_order_line(self) -> None:
        with self.uow as uow:
            raise NotImplementedError

    def get_order_line(self) -> None:
        with self.uow as uow:
            raise NotImplementedError

    def get_all_order_lines(self) -> None:
        with self.uow as uow:
            raise NotImplementedError

    def update_order_line(self) -> None:
        with self.uow as uow:
            raise NotImplementedError

    def delete_order_line(self) -> None:
        with self.uow as uow:
            raise NotImplementedError
