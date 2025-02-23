from datetime import date
from typing import List

from pydantic import BaseModel


class OrderLineSchema(BaseModel):
    order_id: str
    sku: str
    qty: int


class BatchSchema(BaseModel):
    reference: str
    sku: str
    eta: date | None
    available_quantity: int
    allocated_quantity: int
    allocations: List[OrderLineSchema]


class AllocationsListOut(BaseModel):
    items: List[BatchSchema]
    total: int
    offset: int


class AllocationsOut(BaseModel):
    batch_reference: str
    order_line: OrderLineSchema


class Allocations(BaseModel):
    items: List[BatchSchema]


class AllocationsAllocateIn(OrderLineSchema):
    ''''''


class AllocationsAllocateOut(BaseModel):
    batch_reference: str


class AllocationsDeallocateIn(OrderLineSchema):
    ''''''


class AllocationsDeallocateOut(BaseModel):
    batch_reference: str
