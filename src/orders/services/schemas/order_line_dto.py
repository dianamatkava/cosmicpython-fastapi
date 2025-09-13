from pydantic import BaseModel


class OrderLineSchemaDTO(BaseModel):
    order_id: str
    sku: str
    qty: int
