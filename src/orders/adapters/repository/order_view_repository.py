# The Repository pattern is an abstraction over persistent storage

from typing import List

from sqlalchemy.orm import Session

from src.orders.domain.order_read_model import OrderReadModel
from src.shared.repository import AbstractRepository


class OrderViewRepository(AbstractRepository[OrderReadModel]):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get(self, order_id: int) -> OrderReadModel:
        return self.session.query(OrderReadModel).filter_by(order_id=order_id).one()

    def update(
        self, order_id: int, order_line_id: int, product_sku: str, product_qty: int
    ):
        order = self.get(order_id=order_id)
        order.order_line_id = order_line_id
        order.product_sku = product_sku
        order.product_qty = product_qty

    def add(self, order: OrderReadModel) -> None:
        self.session.add(order)

    def list(self) -> List[OrderReadModel]:
        return self.session.query(OrderReadModel).all()

    def delete(self, order_id: int) -> None:
        raise NotImplementedError
