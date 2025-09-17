"""Classical (imperative) mapping."""

from sqlalchemy.orm import registry, relationship

from src.allocations.adapters.orm import allocations
from src.allocations.domain.batch import BatchModel
from src.allocations.domain.product_aggregate import ProductAggregate
from src.inventory.adapters.orm import batches, product
from src.inventory.domain.batch_model import InventoryBatchModel
from src.inventory.domain.product_model import ProductModel
from src.orders.adapters.orm import order_lines
from src.orders.domain.order_line_model import OrderLineModel

mapper_registry = (
    registry()
)  # contains the info about how to map db tables to python models


def start_mappers():
    # Inverting Database Dependency ORM from Domain model
    # Following is the configuration for how to convert between the schema and domain model
    order_lines_mapper = mapper_registry.map_imperatively(OrderLineModel, order_lines)
    inventory_batch_mapper = mapper_registry.map_imperatively(
        InventoryBatchModel, batches
    )
    inventory_product_mapper = mapper_registry.map_imperatively(ProductModel, product)

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

    allocation_batch_mapper = mapper_registry.map_imperatively(
        BatchModel,
        batches,
        properties={
            "_allocations": relationship(
                order_lines_mapper,  # Maps to OrderLineModel
                secondary=allocations,  # Through the 'allocations' join table
                collection_class=set,  # Allocations are stored in a set
            ),
        },
    )
