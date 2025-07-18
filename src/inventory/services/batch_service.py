"""business logic, Accepts only primitives or a minimal DTO"""

from datetime import date
from typing import Optional, List, Tuple

from src.allocations.adapters.uow import AbstractAllocationsUnitOfWork
from src.allocations.domain import batch_domain_model as domain
from src.allocations.services.schemas import AllocationSchemaDTO


class OutOfStock(Exception):
    """OutOfStock Exception"""


class BatchService:
    uow: AbstractAllocationsUnitOfWork

    def __init__(self, uow: AbstractAllocationsUnitOfWork):
        self.uow = uow

    def add_batch(
        self, ref: str, sku: str, qty: int, eta: Optional[date] = None
    ) -> None:
        with self.uow as uow:
            uow.product_repo.add(domain.BatchModel(ref, sku, qty, eta))
            uow.commit()

    def get_batche_by_ref(self, ref: str) -> domain.BatchModel:
        with self.uow as uow:
            return uow.product_repo.get(reference=ref)

    def get_batches(self) -> List[domain.BatchModel]:
        with self.uow as uow:
            return uow.product_repo.list()

    def delete_batch(self, ref: str) -> None:
        with self.uow as uow:
            uow.product_repo.delete(reference=ref)
            uow.commit()

    def get_allocations(self) -> List[domain.OrderLineModel]:
        batches = self.get_batches()
        return [alloc for batch in batches for alloc in batch.allocations]

    def allocate(self, order_line: AllocationSchemaDTO) -> Tuple[str, str]:
        with self.uow as uow:
            order_line_model = domain.OrderLineModel(**order_line.model_dump())
            batches = uow.product_repo.list()
            try:
                batch = next(
                    b for b in sorted(batches) if b.can_allocate(order_line_model)
                )
            except StopIteration as e:
                print(f"Error allocating batches: {e=}")
                raise OutOfStock() from e

            batch.allocate(order_line_model)
            uow.commit()
        return batch.reference, order_line.order_id

    def deallocate(self, order_id: str, batch_reference: str):
        with self.uow as uow:
            batch = uow.product_repo.get(batch_reference)
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
