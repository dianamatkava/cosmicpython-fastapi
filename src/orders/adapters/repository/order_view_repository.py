# The Repository pattern is an abstraction over persistent storage

from typing import List

from pydantic import TypeAdapter
from sqlalchemy.orm import Session

from src.adapters.redisclient import MemStorageClient
from src.orders.domain.order_read_model import OrderReadModel
from src.shared.adapters.repository import AbstractRepository


class OrderViewRepository(AbstractRepository[OrderReadModel]):
    session: Session

    def __init__(self, session: Session, in_mem: MemStorageClient):
        self.session = session
        self.in_mem = in_mem

    def get(self, order_id: int) -> OrderReadModel:
        order = self.in_mem.get_document(f"order:{order_id}")
        if not order:
            order = (
                self.session.query(OrderReadModel).filter_by(order_id=order_id).one()
            )
        return TypeAdapter(OrderReadModel).validate_python(order, from_attributes=True)

    def list(self) -> List[OrderReadModel]:
        orders = self.in_mem.get_documents("order:")
        if not orders:
            orders = self.session.query(OrderReadModel).all()
        return TypeAdapter(List[OrderReadModel]).validate_python(
            orders, from_attributes=True
        )

    def add(self, order: OrderReadModel) -> None:
        raise NotImplementedError

    def delete(self, order_id: int, order_line_id: int) -> None:
        self.session.query(OrderReadModel).filter_by(
            order_id=order_id, order_line_id=order_line_id
        ).delete()
