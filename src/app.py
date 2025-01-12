from typing import Annotated, Any
from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

from db.orm_models import Product

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/test")
def test_route(session: Annotated[Any, Depends(get_session)]):
    products = session.query(Product).all()
    print(products)
    return 201
