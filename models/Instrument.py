from sqlalchemy import Column, Integer, String, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from db.base import Base


class Instrument(Base):
    __tablename__ = 'instruments'
    __table_args__ = (
        UniqueConstraint('ticker', 'symbol_id', 'account_id', name='unique_instrument'),
    )

    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # broker_id = Column(Integer, ForeignKey('brokers.id'))
    # broker = relationship("Broker", back_populates="instruments")

    symbol_id = Column(Integer, ForeignKey('symbols.id'))
    # standard_symbol = relationship("Symbol", back_populates="instruments")

    account_id = Column(Integer, ForeignKey('accounts.id'))
    # account = relationship("Account", back_populates="instruments")

    suffix_id = Column(Integer, ForeignKey('suffixes.id'))
    suffix = relationship('Suffix', backref='instruments')

    trades = relationship("Trade", back_populates="instrument")

    # Metadata
    lot_size = Column(Float, nullable=True)
    leverage = Column(Integer, nullable=True)
    min_volume = Column(Float, nullable=True)
    max_volume = Column(Float, nullable=True)
    step_volume = Column(Float, nullable=True)
