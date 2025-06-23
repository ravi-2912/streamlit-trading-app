import sys
import os
from typing import List
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from models import Broker, Account, PlatformType, Symbol, Instrument, Suffix
from db.get_session import get_session

from data_access.add_instrument import add_instrument



def seed_brokers(clear_existing: bool = True):
    with get_session() as session:
        if clear_existing:
            session.query(Broker).delete()
            session.commit()

        brokers = [
            Broker(name="IC Markets"),
            Broker(name="Pepperstone"),
            Broker(name="FXCM"),
            Broker(name="FTMO"),
            Broker(name="The5ers"),
            Broker(name="E8"),
        ]

        session.add_all(brokers)
        session.commit()
        print("Brokers seeded successfully.")
        return brokers


def seed_accounts(brokers: List[Broker] ,clear_existing: bool = True):
    with get_session() as session:
        if clear_existing:
            session.query(Account).delete()
            session.commit()

        accounts = [
            Account(
                name="IC Markets Demo 1",
                login="52399047",
                password="9UtKTv0!2MUeaT",
                type="demo",
                broker=brokers[0],
                platform=PlatformType.mt5,
                path=os.path.join("D:\\", "MetaTrader5","MT5_MT_1", "terminal64.exe"),
                portable=True,
                server="ICMarketsSC-Demo"
            ),
            Account(
                name="IC Markets Demo 2",
                login="52399298",
                password="10Bf@C4NzJWFUF",
                type="demo",
                broker=brokers[0],
                platform=PlatformType.mt5,
                path=os.path.join("D:\\", "MetaTrader5","MT5_MT_2", "terminal64.exe"),
                portable=True,
                server="ICMarketsSC-Demo",
            ),
            Account(
                name="Pepperstone Spread Betting Demo",
                login="62081926",
                password="?afslF8rqn",
                type="demo",
                broker=brokers[1],
                platform=PlatformType.mt5,
                path=os.path.join("D:\\", "MetaTrader5","MT5_MT_3", "terminal64.exe"),
                portable=True,
                server="PepperstoneUK-Demo",
            ),
        ]

        session.add_all(accounts)
        session.commit()
        print("Accounts seeded successfully.")
        return accounts


def seed_symbols(clear_existing: bool = True):
    with get_session() as session:
        if clear_existing:
            session.query(Symbol).delete()
            session.commit()

        symbols = [
            Symbol(symbol="EURUSD", description="Euro to US Dollar"),
            Symbol(symbol="GBPUSD", description="British Pound to US Dollar"),
            Symbol(symbol="USDJPY", description="US Dollar to Japanese Yen"),
            Symbol(symbol="AUDUSD", description="Australian Dollar to US Dollar"),
            Symbol(symbol="USDCAD", description="US Dollar to Canadian Dollar"),
        ]

        session.add_all(symbols)
        session.commit()
        print("Symbols seeded successfully.")
        return symbols


def seed_instruments(symbols, accounts, clear_existing: bool = True):
    with get_session() as session:
        if clear_existing:
            session.query(Suffix).delete()
            session.query(Instrument).delete()
            session.commit()
        instruments = [
            add_instrument(session, ticker="EURUSD", account=accounts[0]),
            add_instrument(session, ticker="EURUSD.ecn", account=accounts[1]),
            add_instrument(session, ticker="EURUSD_SB", account=accounts[2]),
            add_instrument(session, ticker="EUR_USD", account=accounts[2]),
            add_instrument(session, ticker="EUR_USD.r", account=accounts[2])
        ]
        session.add_all(instruments)
        session.commit()
        # instruments = [
        #     Instrument(
        #         ticker="EURUSD",
        #         description="Euro to US Dollar",
        #         symbol=symbols[0],
        #         account=accounts[0],
        #     ),
        #     Instrument(
        #         ticker="GBPUSD",
        #         description="Euro to US Dollar",
        #         symbol=symbols[1],
        #         account=accounts[0],
        #     ),
        #     Instrument(
        #         ticker="EURUSD.ecn",
        #         description="Euro to US Dollar",
        #         symbol=symbols[0],
        #         account=accounts[1],
        #     ),
        #     Instrument(
        #         ticker="GBPUSD.ecn",
        #         description="Euro to US Dollar",
        #         symbol=symbols[1],
        #         account=accounts[1],
        #     ),
        #     Instrument(
        #         ticker="EURUSD_SB",
        #         description="Euro to US Dollar",
        #         symbol=symbols[0],
        #         account=accounts[2],
        #     ),
        #     Instrument(
        #         ticker="GBPUSD_SB",
        #         description="Euro to US Dollar",
        #         symbol=symbols[1],
        #         account=accounts[2],
        #     ),
        # ]

        # session.add_all(instruments)
        # session.commit()
    print("Instruments seeded successfully.")
        # return instruments



def seed_all():
    brokers = seed_brokers()
    accounts = seed_accounts(brokers)
    symbols = seed_symbols()
    instruments = seed_instruments(symbols, accounts)
    return brokers, accounts, symbols, instruments

if __name__ == "__main__":
    seed_all()
