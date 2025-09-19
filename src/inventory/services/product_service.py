"""business logic, Accepts only primitives or a minimal DTO"""

from typing import Any, List

from src.inventory.adapters.uow import ProductAggregateUnitOfWork
from src.inventory.services.schemas.product_dto import ProductDTO
from src.inventory.services.transformers.product_transformers import (
    transform_product_dto_to_domain_model,
    transform_product_domain_model_to_dto,
)


class ProductService:
    uow: Any

    def __init__(self, uow: ProductAggregateUnitOfWork):
        self.uow = uow

    def create_product(self, product: ProductDTO) -> ProductDTO:
        product_model = transform_product_dto_to_domain_model(product)
        with self.uow as uow:
            uow.product_repo.add(product_model)
            product = uow.product_repo.get(product_model.sku)
            uow.commit()

        return transform_product_domain_model_to_dto(product)

    def get_product(self, sku: str) -> ProductDTO:
        with self.uow as uow:
            product = uow.product_repo.get(sku)

        return transform_product_domain_model_to_dto(product)

    def get_all_products(self) -> List[ProductDTO]:
        with self.uow as uow:
            products = uow.product_repo.list()

        return [transform_product_domain_model_to_dto(product) for product in products]

    def delete_product(self, sku: str) -> None:
        with self.uow as uow:
            uow.product_repo.delete(sku)
            uow.commit()
