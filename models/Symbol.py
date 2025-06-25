from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class Symbol(Base):
    __tablename__ = 'symbols'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    type = Column(String, nullable=True)
    sector = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    country = Column(String, nullable=True)
    currency = Column(String, nullable=True)
    exchange = Column(String, nullable=True)

    instruments = relationship('Instrument', backref='symbol')
    trades = relationship('Trade', back_populates='symbol')