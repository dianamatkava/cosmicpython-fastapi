"""Classical (imperative) mapping."""

from sqlalchemy.orm import registry, relationship

from src.inventory.adapters.orm import allocations, batches, product
from src.inventory.domain.batch import BatchModel
from src.inventory.domain.outbox import OutBoxModel
from src.inventory.domain.product_aggregate import ProductAggregate
from src.orders.adapters.orm import order_lines, order, order_view_model
from src.orders.domain import order_line_model as domain
from src.orders.domain.order_model import OrderModel
from src.orders.domain.order_read_model import OrderReadModel
from src.shared.adapters.orm import outbox

mapper_registry = (
    registry()
)  # contains the info about how to map db tables to python models


def start_mappers():
    # Inverting Database Dependency ORM from Domain model
    # Following is the configuration for how to convert between the schema and domain model
    order_lines_mapper = mapper_registry.map_imperatively(
        domain.OrderLineModel, order_lines
    )
    order_mapper = mapper_registry.map_imperatively(OrderModel, order)
    order_view_mapper = mapper_registry.map_imperatively(
        OrderReadModel, order_view_model
    )
    outbox_mapper = mapper_registry.map_imperatively(OutBoxModel, outbox)
    product_aggregate_mapper = mapper_registry.map_imperatively(
        ProductAggregate,
        product,
        properties={
            "_batches": relationship(
                BatchModel,  # Maps to BatchModel
                collection_class=set,
            ),
        },
    )

    batch_mapper = mapper_registry.map_imperatively(
        BatchModel,
        batches,
        properties={
            "_allocations": relationship(
                order_lines_mapper,  # Maps to OrderLineModel
                secondary=allocations,  # Through the 'inventory' join table
                collection_class=set,  # Allocations are stored in a set
            ),
        },
    )
