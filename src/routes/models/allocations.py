from pydantic import BaseModel

from src.domain.model import OrderLineModel


class AllocationsOut(BaseModel):
    batch_reference: str
    order_line: OrderLineModel


class AllocationsAllocateIn(BaseModel):
    batch_reference: str
    order_line: OrderLineModel


class AllocationsDeallocateIn(BaseModel):
    order_line: OrderLineModel
