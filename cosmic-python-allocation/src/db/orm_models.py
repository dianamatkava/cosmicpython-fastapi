from typing import Optional

from sqlmodel import SQLModel, Field


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)


class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    address: str = Field(max_length=255)


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key='customer.id')


class OrderLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    qty: int = Field(default=0)
    order_id: int = Field(foreign_key="order.id")


class Batch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ref: str = Field(max_length=255)
    product_id: int = Field(foreign_key="product.id")
