import datetime

from sqlalchemy import Column, DateTime, Integer, String

from extensions import db


class CustomerData(db.Model):
    __tablename__ = 'arb-user-data'
    id = Column(Integer(), primary_key=True)
    full_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(16), nullable=False)
    datetime = Column('Created on', DateTime, default=datetime.datetime.now)

    def __repr__(self) -> str:
        return f"{self.full_name}"
    