from src.inventory.domain.product_aggregate import ProductAggregate
from src.inventory.services.schemas.product_dto import ProductDTO


def transform_product_dto_to_domain_model(product: ProductDTO) -> ProductAggregate:
    return ProductAggregate(sku=product.sku)


def transform_product_domain_model_to_dto(product: ProductAggregate) -> ProductDTO:
    return ProductDTO(sku=product.sku)
