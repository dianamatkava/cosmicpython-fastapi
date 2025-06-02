from src.domain import batch_domain_model as domain
from src.routes.schemas.allocations import BatchSchema, OrderLineSchema


def transform_batch_to_batch_schema(batch: domain.BatchModel) -> BatchSchema:
    return BatchSchema(
        reference=batch.reference,
        sku=batch.sku,
        eta=batch.eta,
        available_quantity=batch.available_quantity,
        allocated_quantity=batch.allocated_quantity,
        allocations=[
            OrderLineSchema(
                order_id=allocation.order_id, sku=allocation.sku, qty=allocation.qty
            )
            for allocation in batch.allocations
        ],
    )
