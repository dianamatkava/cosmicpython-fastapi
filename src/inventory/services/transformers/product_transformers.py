from src.inventory.domain.product_model import ProductModel
from src.inventory.services.schemas.product_dto import ProductDTO


def transform_product_dto_to_domain_model(product: ProductDTO) -> ProductModel:
    return ProductModel(sku=product.sku)


def transform_product_domain_model_to_dto(product: ProductModel) -> ProductDTO:
    return ProductDTO(sku=product.sku)
