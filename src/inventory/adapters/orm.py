"""Classical (imperative) mapping."""

from sqlalchemy import Column, Integer, Table, ForeignKey

from src.adapters.db_metadata import metadata

allocations = Table(
    "inventory",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", ForeignKey("order_lines.id"), unique=True),
    Column("batch_id", ForeignKey("batches.id")),
)
