import MetaTrader5 as mt5
from datetime import datetime



class MT5Client:
    def __init__(self, name, path, login, password, server):
        self.name = name
        self.path = path
        self.login = login
        self.password = password
        self.server = server
        self.connected = self._connect()

    def _connect(self):
        if not mt5.initialize(path=self.path, portable=True):
            print(f"[{self.name}] Initialization failed: {mt5.last_error()}")
            return False

        authorized = mt5.login(login=self.login, password=self.password, server=self.server)
        if not authorized:
            print(f"[{self.name}] Login failed: {mt5.last_error()}")
            return False

        print(f"[{self.name}] Connected to account {self.login}")
        return True

    def shutdown(self):
        mt5.shutdown()
        print(f"[{self.name}] Disconnected")

    def get_account_info(self):
        info = mt5.account_info()
        return info._asdict() if info else None

    def get_price(self, symbol):
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            print(f"[{self.name}] Failed to get price for {symbol}")
            return None
        return {
            "symbol": symbol,
            "bid": tick.bid,
            "ask": tick.ask,
            "time": datetime.fromtimestamp(tick.time)
        }

    def place_order(self, symbol, lot, order_type='buy', price=None, sl=None, tp=None, magic=1000):
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None or not symbol_info.visible:
            mt5.symbol_select(symbol, True)

        if order_type.lower() == 'buy':
            order_type_enum = mt5.ORDER_TYPE_BUY
            price = price or mt5.symbol_info_tick(symbol).ask
        elif order_type.lower() == 'sell':
            order_type_enum = mt5.ORDER_TYPE_SELL
            price = price or mt5.symbol_info_tick(symbol).bid
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

        result = mt5.order_send(request)
        return result._asdict()

    def close_trade(self, ticket):
        position = mt5.positions_get(ticket=ticket)
        if not position:
            print(f"[{self.name}] Trade not found: {ticket}")
            return None

        pos = position[0]
        price = mt5.symbol_info_tick(pos.symbol).ask if pos.type == mt5.POSITION_TYPE_SELL else mt5.symbol_info_tick(pos.symbol).bid
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

        result = mt5.order_send(request)
        return result._asdict()

    def modify_trade(self, ticket, sl=None, tp=None):
        position = mt5.positions_get(ticket=ticket)
        if not position:
            print(f"[{self.name}] Trade not found: {ticket}")
            return None

        pos = position[0]
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "sl": sl,
            "tp": tp,
            "magic": pos.magic
        }

        result = mt5.order_send(request)
        return result._asdict()



if __name__ == "__main__":
    accounts = [
        {
            "name": "Account1",
            "path": "D:/MetaTrader5/MT_1/terminal64.exe",
            "login": 52399047,
            "password": "9UtKTv0!2MUeaT",
            "server": "ICMarketsSC-Demo"
        },
        {
            "name": "Account2",
            "path": "D:/MetaTrader5/MT_2/terminal64.exe",
            "login": 52399298,
            "password": "10Bf@C4NzJWFUF",
            "server": "ICMarketsSC-Demo"
        }
    ]

    clients = []
    for acc in accounts:
        client = MT5Client(**acc)
        if client.connected:
            print(client.get_account_info())
            print(client.get_price("EURUSD"))
            # Example: Place a 0.01 lot buy
            # print(client.place_order("EURUSD", 0.01, "buy"))

        # clients.append(client)

    # Graceful shutdown
    for c in clients:
        c.shutdown()
