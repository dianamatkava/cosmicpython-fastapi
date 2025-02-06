from typing import List

from pydantic import BaseModel

from src.domain import model


class AllocationsOut(BaseModel):
    batch_reference: str
    order_line: model.OrderLineModel


class Allocations(BaseModel):
    items: List[model.BatchModel]


class AllocationsAllocateIn(BaseModel):
    order_line: model.OrderLineModel


class AllocationsAllocateOut(BaseModel):
    batch_reference: str


class AllocationsDeallocateIn(BaseModel):
    order_line: model.OrderLineModel


class AllocationsDeallocateOut(BaseModel):
    batch_reference: str
