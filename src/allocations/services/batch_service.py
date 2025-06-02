"""business logic, Accepts only primitives or a minimal DTO"""

from datetime import date
from typing import Optional, List

from src.allocations.adapters.uow import AbstractUnitOfWork
from src.allocations.domain import batch_domain_model as domain
from src.allocations.services.schemas import AllocationSchemaDTO


class OutOfStock(Exception):
    """OutOfStock Exception"""


class BatchService:
    uow: AbstractUnitOfWork

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def add_batch(
        self, ref: str, sku: str, qty: int, eta: Optional[date] = None
    ) -> None:
        with self.uow as uow:
            uow.batch_repo.add(domain.BatchModel(ref, sku, qty, eta))
            uow.commit()

    def get_batche_by_ref(self, ref: str) -> domain.BatchModel:
        with self.uow as uow:
            return uow.batch_repo.get(reference=ref)

    def get_batches(self) -> List[domain.BatchModel]:
        with self.uow as uow:
            return uow.batch_repo.list()

    def delete_batch(self, ref: str) -> None:
        with self.uow as uow:
            uow.batch_repo.delete(reference=ref)
            uow.commit()

    def get_allocations(self) -> List[domain.OrderLineModel]:
        batches = self.get_batches()
        return [alloc for batch in batches for alloc in batch.allocations]

    def allocate(self, order_line: AllocationSchemaDTO) -> str:
        with self.uow as uow:
            order_line_model = domain.OrderLineModel(**order_line.model_dump())
            batches = uow.batch_repo.list()
            try:
                batch = next(
                    b for b in sorted(batches) if b.can_allocate(order_line_model)
                )
            except StopIteration as e:
                print(f"Error allocating batches: {e=}")
                raise OutOfStock() from e

            batch.allocate(order_line_model)
            uow.commit()
        return batch.reference

    def deallocate(self, order_id: str, batch_reference: str):
        with self.uow as uow:
            batch = uow.batch_repo.get(batch_reference)
            try:
                order_line_model = next(
                    allocation
                    for allocation in batch.allocations
                    if allocation.order_id == order_id
                )
            except StopIteration:
                raise ModuleNotFoundError
            batch.deallocate(order_line_model)
            uow.commit()
