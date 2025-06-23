import re
from typing import Optional, Tuple

from models import Symbol


def extract_symbol_and_suffix2(ticker: str, all_symbols: list[Symbol]) -> Tuple[Optional[Symbol], Optional[str]]:
    """Return (matched Symbol object, suffix with original separator) from a given ticker."""
    # Remove separators for matching
    cleaned_ticker = re.sub(r'[\._\-]', '', ticker.upper())

    # Find the matched symbol
    matched_symbol_obj = next(
        (s for s in all_symbols if s.symbol.upper() in cleaned_ticker),
        None
    )
    if not matched_symbol_obj:
        return None, None

    cleaned_symbol = matched_symbol_obj.symbol.upper()
    index_in_cleaned = cleaned_ticker.find(cleaned_symbol)
    if index_in_cleaned == -1:
        return matched_symbol_obj, None, None

    # Map positions of non-separator characters from ticker to cleaned
    cleaned = ''
    mapping = []  # mapping[i] = index in original ticker
    for i, c in enumerate(ticker):
        if c not in '._-':
            mapping.append(i)
            cleaned += c

    symbol_end_in_cleaned = index_in_cleaned + len(cleaned_symbol)
    if symbol_end_in_cleaned >= len(mapping):
        return matched_symbol_obj, None, None

    # Start suffix extraction from the character *after* the last matched symbol character in original ticker
    suffix_start_index = mapping[symbol_end_in_cleaned - 1] + 1
    suffix = ticker[suffix_start_index:]
    suffix_tag = suffix[1:]

    return matched_symbol_obj, suffix, suffix_tag if suffix else None
