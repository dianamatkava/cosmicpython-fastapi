from src.inventory.services.schemas.product_dto import ProductDTO
from src.register.domain.product_model import ProductModel


def transform_product_dto_to_domain_model(product: ProductDTO) -> ProductModel:
    return ProductModel(sku=product.sku)


def transform_product_domain_model_to_dto(product: ProductModel) -> ProductDTO:
    return ProductDTO(sku=product.sku)
