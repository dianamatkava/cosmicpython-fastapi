from typing import Annotated, List

from fastapi import APIRouter, Path, Depends, Body
from pydantic import TypeAdapter
from starlette import status

from src.inventory.conf import get_product_service
from src.inventory.routes.schemas.request_models.product import ProductDataRequestModel
from src.inventory.routes.schemas.response_models.product import (
    ProductDataResponseModel,
)
from src.inventory.services.product_service import ProductService

router = APIRouter(prefix="/product", tags=["product"])
# TODO: Management Auth


@router.get(
    "/{sku}", status_code=status.HTTP_200_OK, response_model=ProductDataResponseModel
)
def get_product(
    sku: Annotated[str, Path(..., description="Identifier of the product.")],
    product_service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductDataResponseModel:
    return TypeAdapter(ProductDataResponseModel).validate_python(
        product_service.get_product(sku=sku), from_attributes=True
    )


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=List[ProductDataResponseModel]
)
def list_products(
    product_service: Annotated[ProductService, Depends(get_product_service)],
) -> List[ProductDataResponseModel]:
    products = product_service.get_all_products()
    return TypeAdapter(List[ProductDataResponseModel]).validate_python(
        products, from_attributes=True
    )


@router.post(
    "", status_code=status.HTTP_200_OK, response_model=ProductDataResponseModel
)
def create_product(
    product_data: Annotated[
        ProductDataRequestModel,
        Body(..., description="Request Model to create product."),
    ],
    product_service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductDataResponseModel:
    product = product_service.create_product(product=product_data)
    return TypeAdapter(ProductDataResponseModel).validate_python(
        product, from_attributes=True
    )


@router.delete("/{sku}", status_code=status.HTTP_200_OK)
def delete_product(
    sku: Annotated[str, Path(..., description="Identifier of the product.")],
    product_service: Annotated[ProductService, Depends(get_product_service)],
):
    product_service.delete_product(sku=sku)
