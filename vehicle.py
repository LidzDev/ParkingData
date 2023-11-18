from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)

Vehicle.__table__