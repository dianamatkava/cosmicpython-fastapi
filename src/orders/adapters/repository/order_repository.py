# The Repository pattern is an abstraction over persistent storage

from typing import List

from sqlalchemy.orm import Session

from src.orders.domain.order_model import OrderModel
from src.shared.repository import AbstractRepository


class OrderRepository(AbstractRepository[OrderModel]):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get(self, id: int) -> OrderModel:
        return self.session.query(OrderModel).filter_by(id=id).one()

    def add(self, order: OrderModel) -> None:
        self.session.add(order)

    def list(self) -> List[OrderModel]:
        return self.session.query(OrderModel).all()

    def delete(self, id: int) -> None:
        self.session.query(OrderModel).filter_by(id=id).delete()
