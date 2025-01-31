from sqlalchemy import text

from src.tests.conftest import session
from src.domain import model


def test_get_products(session):
    insert_query = text("""
        INSERT INTO ProductModel (name) VALUES 
        ("RED-CHAIR"),
        ("RED-TABLE"),
        ("BLUE-LIPSTICK")
    """)

    session.execute(insert_query)

    expected_products = [
        model.ProductModel(sku='1', name='RED-CHAIR'),
        model.ProductModel(sku='2', name='RED-TABLE'),
        model.ProductModel(sku='3', name='BLUE-LIPSTICK')
    ]

    assert session.query(model.ProductModel).all() == expected_products


