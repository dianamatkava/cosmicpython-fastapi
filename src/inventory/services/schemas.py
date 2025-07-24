"""Consumes domain models, enforces business logic, and returns domain instances or slim DTOs."""

from datetime import date

from pydantic import BaseModel


class BatchSchemaDTO(BaseModel):
    reference: str
    sku: str
    eta: date | None
    available_quantity: int
    allocated_quantity: int
