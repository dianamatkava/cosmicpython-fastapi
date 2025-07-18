"""Consumes domain models, enforces business logic, and returns domain instances or slim DTOs."""

from pydantic import BaseModel


class OrderLineSchemaDTO(BaseModel):
    order_id: str
    sku: str
    qty: int
