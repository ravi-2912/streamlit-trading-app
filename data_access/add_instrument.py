from db.get_session import get_session
from models import Instrument, Suffix, Symbol
from utils.ticker import extract_symbol_and_suffix2


def add_instrument(session, **kwargs) -> Instrument:
    ticker = kwargs.get("ticker")
    symbols = session.query(Symbol).all()
    symbol, suffix_name, suffix_tag = extract_symbol_and_suffix2(ticker, symbols)
    suffix = session.query(Suffix).filter_by(name=suffix_name).first()
    if not suffix and suffix_name:
        suffix = Suffix(name=suffix_name, tag=suffix_tag)
        session.add(suffix)
    # if not symbol:
    #     raise ValueError(f"Symbol not found for ticker: {ticker}")
    instrument = Instrument(**kwargs, symbol=symbol, suffix=suffix)
    return instrument
