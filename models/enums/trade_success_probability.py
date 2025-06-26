from enum import Enum


class TradeSuccessProbabilityType(str, Enum):
    very_high = "Very High"
    high = "High"
    medium = "Medium"
    low = "Low"
