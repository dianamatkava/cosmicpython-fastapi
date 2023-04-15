from extensions import db
from sqlalchemy import Column, Integer, String

class CustomerData(db.Model):
    __tablename__ = 'arb-user-data'
    id = Column(Integer(), primary_key=True)
    full_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(16), nullable=False)

    def __repr__(self) -> str:
        return f"{self.full_name}"
    