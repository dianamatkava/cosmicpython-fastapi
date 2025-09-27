"""Classical (imperative) mapping."""

from sqlalchemy import Column, Integer, Table, ForeignKey

from src.database.metadata import metadata

order = Table(
    "order",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
)


order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", ForeignKey("order.id"), doc="Reference to a order"),
    Column("sku", ForeignKey("product.sku"), doc="Reference to a product"),
    Column("qty", Integer, nullable=False),
)
