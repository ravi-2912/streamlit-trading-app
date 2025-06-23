from enum import Enum
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class Broker(Base):
    __tablename__ = 'brokers'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    accounts = relationship("Account", back_populates="broker")

    # symbol_mappings = relationship("SymbolMapping", back_populates="broker")
