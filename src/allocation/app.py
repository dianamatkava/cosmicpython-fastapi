from typing import Annotated, Any

from fastapi import Depends, FastAPI

from src.allocation.adapters.orm_models import Product
from src.allocation.conf import get_session, create_db_and_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def home(session: Annotated[Any, Depends(get_session)]):
    products = session.query(Product).all()
    print(products)
    return 201
