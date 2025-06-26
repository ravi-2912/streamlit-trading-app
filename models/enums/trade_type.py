from enum import Enum


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
