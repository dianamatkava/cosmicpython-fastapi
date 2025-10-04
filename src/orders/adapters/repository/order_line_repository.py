# The Repository pattern is an abstraction over persistent storage

from typing import List

from sqlalchemy.orm import Session

from src.orders.domain import order_line_model as domain
from src.shared.repository import AbstractRepository


class OrderLineRepository(AbstractRepository[domain.OrderLineModel]):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get(self, id: int) -> domain.OrderLineModel:
        return self.session.query(domain.OrderLineModel).filter_by(id=id).one()

    def add(self, order_line: domain.OrderLineModel) -> None:
        self.session.add(order_line)

    def list(self) -> List[domain.OrderLineModel]:
        return self.session.query(domain.OrderLineModel).all()

    def delete(self, id: int) -> None:
        self.session.query(domain.OrderLineModel).filter_by(id=id).delete()
