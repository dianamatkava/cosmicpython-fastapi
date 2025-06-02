from datetime import date
from typing import Optional, List

from src.adapters.uow import AbstractUnitOfWork
from src.domain import batch_domain_model as domain
from src.routes.schemas.allocations import AllocationsListOut, OrderLineSchema
from src.services.transformers.batch_transformers import transform_batch_to_batch_schema


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

    def get_allocations(self) -> AllocationsListOut:
        with self.uow as uow:
            batches = uow.batch_repo.list()
        return AllocationsListOut(
            items=[transform_batch_to_batch_schema(b) for b in batches],
            total=len(batches),
            offset=10,
        )

    def allocate(self, order_line: OrderLineSchema) -> str:
        with self.uow as uow:
            order_line_model = domain.OrderLineModel(**order_line.model_dump())
            batches = uow.batch_repo.list()
            try:
                batch = next(
                    b for b in sorted(batches) if b.can_allocate(order_line_model)
                )
            except StopIteration as e:
                print(f"Error allocating batches: {e}")
                raise OutOfStock() from e

            batch.allocate(order_line_model)
            uow.commit()
        return batch.reference

    def deallocate(self, order_line: OrderLineSchema, batch_reference: str):
        with self.uow as uow:
            order_line_model = domain.OrderLineModel(**order_line.model_dump())
            batch = uow.batch_repo.get(batch_reference)
            batch.deallocate(order_line_model)
            uow.commit()
