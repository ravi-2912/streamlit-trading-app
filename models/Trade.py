from enum import Enum
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from db.base import Base

class DirectionType(str, Enum):
    long = "Long"
    short = "Short"

class OrderType(str, Enum):
    market = "Market"
    limit = "Limit"
    stop = "Stop"

class TradeStatusType(str, Enum):
    active = "Active"
    pending = "Pending"
    closed = "Closed"

class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)

    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    account = relationship("Account", back_populates="trades")
    symbol_id = Column(String, ForeignKey('symbols.symbol'), nullable=False)
    symbol = relationship("Symbol", back_populates="trades")
    instrument_id = Column(Integer, ForeignKey('instruments.id'), nullable=False)
    instrument = relationship("Instrument", back_populates="trades")
    strategy_id = Column(Integer, ForeignKey('strategies.id'), nullable=True)
    strategy = relationship("Strategy", back_populates="trades")

    status = Column(SQLAlchemyEnum(TradeStatusType), nullable=False)

    risk = Column(Float, nullable=False)

    direction = Column(SQLAlchemyEnum(DirectionType), nullable=False)
    order_type = Column(SQLAlchemyEnum(OrderType), nullable=False)
    lots = Column(Float, nullable=False)
    units = Column(Integer, nullable=False)
    entry_price = Column(Float, nullable=False)
    stop_loss_pips = Column(Float, nullable=True)
    take_profit_pips = Column(Float, nullable=True)
    stop_loss_price = Column(Float, nullable=True)
    take_profit_price = Column(Float, nullable=True)
    open_time = Column(DateTime, nullable=False)
    exit_time = Column(DateTime, nullable=True)
    exit_price = Column(Float, nullable=True)

    duration = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    reward_risk = Column(Float, nullable=True)
    exit_reason = Column(String, nullable=True)
    exit_reason_details = Column(String, nullable=True)
    comments = Column(String, nullable=True)

    notes = Column(String, nullable=True) # possibly a separate table

    # ids returned by the MT5 or CT5
