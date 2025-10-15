# The Repository pattern is an abstraction over persistent storage

from typing import List

from sqlalchemy.orm import Session

from src.orders.domain.order_model import OrderModel
from src.shared.adapters.repository import AbstractRepository


class OrderRepository(AbstractRepository[OrderModel]):
    session: Session
    seen: List[OrderModel]

    def __init__(self, session: Session):
        self.session = session
        self.seen = []

    def get(self, id: int) -> OrderModel:
        return self.session.query(OrderModel).filter_by(id=id).one()

    def add(self, order: OrderModel) -> None:
        self.session.add(order)
        self.seen.append(order)

    def list(self) -> List[OrderModel]:
        return self.session.query(OrderModel).all()

    def delete(self, id: int) -> None:
        order = self.get(id=id)
        self.seen.append(order)
        order.delete()
