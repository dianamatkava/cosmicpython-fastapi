from sqlalchemy import text
from sqlmodel import Session

from cruds.product_crud import ProductCrud
from db.orm_models import Product


def test_create_product(session: Session, product_crud: ProductCrud):
    product_crud.create("BUE-TABLE")
    products = session.query(Product).all()
    expected_products = [Product(name="BUE-TABLE", id=1)]
    assert expected_products == products


def test_get_product(session: Session, product_crud: ProductCrud):
    insert_query = text("""
        INSERT INTO product (name) VALUES 
        ("RED-CHAIR")
    """)
    session.execute(insert_query)

    product = product_crud.get_by_id(id=1)
    expected_product = Product(id=1, name="RED-CHAIR")
    assert expected_product == product
