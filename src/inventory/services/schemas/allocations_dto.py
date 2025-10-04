from pydantic import BaseModel


class AllocationSchemaDTO(BaseModel):
    order_id: int
    sku: str
    qty: int
