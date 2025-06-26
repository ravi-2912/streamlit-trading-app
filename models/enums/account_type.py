from enum import Enum


class AccountType(str, Enum):
    demo = "Demo"
    live = "Live"


class PlatformType(str, Enum):
    mt5 = "MT5"
    mt4 = "MT4"
    ct5 = "cT5"
