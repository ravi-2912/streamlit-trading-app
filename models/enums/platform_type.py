from enum import Enum


class PlatformType(str, Enum):
    mt5 = "MT5"
    mt4 = "MT4"
    ct5 = "cT5"
