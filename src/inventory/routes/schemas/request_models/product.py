from typing import Annotated

from pydantic import Field

from src.inventory.services.schemas.product_dto import ProductDTO


class ProductDataRequestModel(ProductDTO):
    sku: Annotated[str, Field(..., description="Identifier of the product.")]
