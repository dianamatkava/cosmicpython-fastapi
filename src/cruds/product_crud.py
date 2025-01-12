# The Repository pattern is an abstraction over persistent storage
from sqlmodel import Session

from db.orm_models import Product


class ProductCrud:

    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Product:
        return self.session.query(Product).get(id)

    def create(self, name: str) -> Product:
        product = Product(name=name)
        self.session.add(product)
        return product
