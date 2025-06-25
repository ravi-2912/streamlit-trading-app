from enum import Enum


class CurrencyType(str, Enum):
    # Major currencies (most traded globally)
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CHF = "CHF"
    AUD = "AUD"
    CAD = "CAD"
    NZD = "NZD"

    # Minor currencies (frequently traded but less liquid than majors)
    CNY = "CNY"
    HKD = "HKD"
    NOK = "NOK"
    SGD = "SGD"
    KRW = "KRW"
    SEK = "SEK"
    MXN = "MXN"

    # Exotic currencies (less traded, more volatile)
    # INR = "INR"
    # IDR = "IDR"
    # MYR = "MYR"
    # PHP = "PHP"
    # THB = "THB"
    # TRY = "TRY"
    # VND = "VND"
    # ZAR = "ZAR"
    # RUB = "RUB"

    # Crypto (optional, not fiat)
    # BTC = "BTC"
    # ETH = "ETH"