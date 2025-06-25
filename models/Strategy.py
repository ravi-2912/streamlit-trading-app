from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base

class Strategy(Base):
    __tablename__ = 'strategies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tag = Column(String, nullable=True)
    description = Column(String, nullable=True)

    trades = relationship("Trade", back_populates="strategy")