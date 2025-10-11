"""Classical (imperative) mapping."""

from enum import StrEnum

from sqlalchemy import Column, Integer, Table, ForeignKey, String

from src.database.metadata import metadata


# TODO: AT-709 Create Base model with created_at, updated_at


class OrderStatus(StrEnum):
    IN_PROCESS = "IN_PROGRESS"
    PAID = "PAID"
    SHIPPED = "SHIPPED"


order = Table(
    "order",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("status", String(255), default=OrderStatus.IN_PROCESS),
)


order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", ForeignKey("order.id"), doc="Reference to a order"),
    Column("sku", ForeignKey("product.sku"), doc="Reference to a product"),
    Column("qty", Integer, nullable=False),
    # Column("purchase_price", Integer, nullable=False),
)


# Denormalized read model, customer facing
# Command-Query Responsibility Segregation (CQRS) Pattern
order_view_model = Table(
    "order_view_model",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", Integer),
    Column("order_status", String(255), default=OrderStatus.IN_PROCESS),
    Column("order_line_id", Integer, unique=True, nullable=False),
    Column("product_sku", String(255), nullable=False, doc="Reference to a product"),
    Column("product_qty", Integer, nullable=False),
)
