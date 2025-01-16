from sqlalchemy import text

from src.allocation.tests.conftest import session
from src.allocation.adapters.orm_models import Product


def test_get_products(session):
    insert_query = text("""
        INSERT INTO product (name) VALUES 
        ("RED-CHAIR"),
        ("RED-TABLE"),
        ("BLUE-LIPSTICK")
    """)

    session.execute(insert_query)

    expected_products = [
        Product(id=1, name='RED-CHAIR'),
        Product(id=2, name='RED-TABLE'),
        Product(id=3, name='BLUE-LIPSTICK')
    ]

    assert session.query(Product).all() == expected_products


