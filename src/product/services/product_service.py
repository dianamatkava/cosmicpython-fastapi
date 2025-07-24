"""business logic, Accepts only primitives or a minimal DTO"""

from typing import Any


class OrderLineService:
    uow: Any

    def __init__(self, uow: Any):
        self.uow = uow

    def create_product(self) -> None:
        with self.uow as uow:
            raise NotImplementedError

    def get_product(self) -> None:
        with self.uow as uow:
            raise NotImplementedError

    def get_all_products(self) -> None:
        with self.uow as uow:
            raise NotImplementedError

    def update_product(self) -> None:
        with self.uow as uow:
            raise NotImplementedError

    def delete_product(self) -> None:
        with self.uow as uow:
            raise NotImplementedError
