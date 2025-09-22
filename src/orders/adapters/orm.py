"""Classical (imperative) mapping."""

from sqlalchemy import Column, Integer, String, Table

from src.database.db_metadata import metadata

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", String(255)),
    Column("sku", String(255), doc="Reference to an product"),
    Column("qty", Integer, nullable=False),
)
