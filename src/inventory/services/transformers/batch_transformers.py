from src.allocations.domain import batch_domain_model as domain
from src.allocations.services.schemas import AllocationSchemaDTO, BatchSchemaDTO


def transform_batch_to_batch_schema(batch: domain.BatchModel) -> BatchSchemaDTO:
    return BatchSchemaDTO(
        reference=batch.reference,
        sku=batch.sku,
        eta=batch.eta,
        available_quantity=batch.available_quantity,
        allocated_quantity=batch.allocated_quantity,
        allocations=[
            AllocationSchemaDTO(
                order_id=allocation.order_id, sku=allocation.sku, qty=allocation.qty
            )
            for allocation in batch.allocations
        ],
    )
