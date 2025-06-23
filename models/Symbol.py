from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class Symbol(Base):
    __tablename__ = 'symbols'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True, nullable=False)
    description = Column(String)

    instruments = relationship('Instrument', backref='symbol')