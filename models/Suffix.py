
from sqlalchemy import Column, Integer, String

from db.base import Base

class Suffix(Base):
    __tablename__ = 'suffixes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tag = Column(String, nullable=True)
    description = Column(String, nullable=True)