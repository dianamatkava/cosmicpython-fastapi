from typing import List

from sqlmodel import Session

from src.adapters.repository import BatchRepository
from src.domain import model
from src.domain.model import OrderLineModel, BatchModel


class OutOfStock(Exception):
    """OutOfStock Exception"""


class BatchService:

    session: Session
    batch_repository: BatchRepository

    def __init__(self, session: Session, batch_repository: BatchRepository):
        self.session = session
        self.batch_repository = batch_repository

    def get_allocations(self) -> List[model.BatchModel]:
        return self.batch_repository.list()

    def allocate(self, order_line: OrderLineModel) -> str:
        batches = self.batch_repository.list()
        try:
            batch = next(b for b in sorted(batches) if b.can_allocate(order_line))
        except StopIteration as e:
            print(f"Error allocating batches: {e}")
            raise OutOfStock() from e

        batch.allocate(order_line)
        return batch.reference

    def deallocate(self, order_line, batch_reference: str):
        batch = self.batch_repository.get(batch_reference)
        batch.deallocate(order_line)
