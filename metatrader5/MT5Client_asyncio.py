import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import MetaTrader5 as mt5
import asyncio
from datetime import datetime
from logger.setup import setup_logger

logger = setup_logger("MT5Client")

class MT5Client:
    def __init__(self, name, path, login, password, server):
        self.name = name
        self.path = path
        self.login = login
        self.password = password
        self.server = server
        self.connected = False

    async def connect(self):
        initialized = await asyncio.to_thread(mt5.initialize, path=self.path, portable=True)
        if not initialized:
            logger.error(f"[{self.name}] Initialization failed: {mt5.last_error()}")
            return False

        authorized = await asyncio.to_thread(mt5.login, self.login, self.password, self.server)
        if not authorized:
            logger.error(f"[{self.name}] Login failed: {mt5.last_error()}")
            return False

        self.connected = True
        logger.info(f"[{self.name}] Connected to account {self.login}")
        return True

    async def shutdown(self):
        await asyncio.to_thread(mt5.shutdown)
        logger.info(f"[{self.name}] Disconnected")
        self.connected = False

    async def get_account_info(self):
        info = await asyncio.to_thread(mt5.account_info)
        return info._asdict() if info else None

    async def get_price(self, symbol):
        tick = await asyncio.to_thread(mt5.symbol_info_tick, symbol)
        if tick is None:
            logger.error(f"[{self.name}] Failed to get price for {symbol}")
            return None
        return {
            "symbol": symbol,
            "bid": tick.bid,
            "ask": tick.ask,
            "time": datetime.fromtimestamp(tick.time)
        }

    async def place_order(self, symbol, lot, order_type='buy', price=None, sl=None, tp=None, magic=1000):
        symbol_info = await asyncio.to_thread(mt5.symbol_info, symbol)
        if symbol_info is None or not symbol_info.visible:
            await asyncio.to_thread(mt5.symbol_select, symbol, True)

        tick = await asyncio.to_thread(mt5.symbol_info_tick, symbol)
        if order_type.lower() == 'buy':
            order_type_enum = mt5.ORDER_TYPE_BUY
            price = price or tick.ask
        elif order_type.lower() == 'sell':
            order_type_enum = mt5.ORDER_TYPE_SELL
            price = price or tick.bid
        else:
            raise ValueError("Invalid order_type. Use 'buy' or 'sell'.")

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": order_type_enum,
            "price": price,
            "sl": sl,
            "tp": tp,
            "magic": magic,
            "deviation": 10,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }

        result = await asyncio.to_thread(mt5.order_send, request)
        return result._asdict()

    async def close_trade(self, ticket):
        position = await asyncio.to_thread(mt5.positions_get, ticket=ticket)
        if not position:
            logger.error(f"[{self.name}] Trade not found: {ticket}")
            return None

        pos = position[0]
        tick = await asyncio.to_thread(mt5.symbol_info_tick, pos.symbol)
        price = tick.ask if pos.type == mt5.POSITION_TYPE_SELL else tick.bid
        close_type = mt5.ORDER_TYPE_BUY if pos.type == mt5.POSITION_TYPE_SELL else mt5.ORDER_TYPE_SELL

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": pos.symbol,
            "volume": pos.volume,
            "type": close_type,
            "position": ticket,
            "price": price,
            "magic": pos.magic,
            "deviation": 10,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = await asyncio.to_thread(mt5.order_send, request)
        return result._asdict()

    async def modify_trade(self, ticket, sl=None, tp=None):
        position = await asyncio.to_thread(mt5.positions_get, ticket=ticket)
        if not position:
            logger.error(f"[{self.name}] Trade not found: {ticket}")
            return None

        pos = position[0]
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "sl": sl,
            "tp": tp,
            "magic": pos.magic
        }

        result = await asyncio.to_thread(mt5.order_send, request)
        return result._asdict()

    async def get_all_symbols(self):
        symbols = await asyncio.to_thread(mt5.symbols_get)
        if not symbols:
            logger.error(f"[{self.name}] Failed to retrieve symbols")
            return []
        return [s.name for s in symbols]


if __name__ == "__main__":

    accounts = [
        # {
        #     "name": "Account1",
        #     "path": "D:/MetaTrader5/MT_1/terminal64.exe",
        #     "login": 52399047,
        #     "password": "9UtKTv0!2MUeaT",
        #     "server": "ICMarketsSC-Demo"
        # },
        # {
        #     "name": "Account2",
        #     "path": "D:/MetaTrader5/MT_2/terminal64.exe",
        #     "login": 52399298,
        #     "password": "10Bf@C4NzJWFUF",
        #     "server": "ICMarketsSC-Demo"
        # },
        {
            "name": "Account3",
            "path": "D:/MetaTrader5/MT_3/terminal64.exe",
            "login": 62081926,
            "password": "?afslF8rqn",
            "server": "PepperstoneUK-Demo"
        },
    ]

    async def handle_account(config):
        client = MT5Client(**config)
        await client.connect()
        if client.connected:
            info = await client.get_account_info()
            price = await client.get_price("EURUSD")
            print(f"[{config['name']}] Account: {info['login']}, Balance: {info['balance']}")
            print(f"[{config['name']}] Price: {price}")
            symbols = await client.get_all_symbols()
            print(f"[{config['name']}] Symbols: {symbols}")
            await client.shutdown()


    async def main():
        await asyncio.gather(*(handle_account(acc) for acc in accounts))


if __name__ == "__main__":
    asyncio.run(main())