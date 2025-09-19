from pydantic import BaseModel


class AllocationSchemaDTO(BaseModel):
    order_id: str
    sku: str
    qty: int
