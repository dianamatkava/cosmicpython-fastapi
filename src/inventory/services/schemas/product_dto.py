from pydantic import BaseModel


class ProductDTO(BaseModel):
    sku: str
