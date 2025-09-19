from pydantic import BaseModel


class AllocationSchemaDTO(BaseModel):
    order_line_id: str

