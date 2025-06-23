import MetaTrader5 as mt5

from difflib import get_close_matches
from models import (
    Base, Broker, Symbol, SymbolMapping,
    Account, AccountSymbolOverride
)

# ---------- Database Setup ----------

# ---------- Utility Functions ----------

def fuzzy_match_standard_symbol(broker_symbol: str, standard_symbols: dict) -> str | None:
    matches = get_close_matches(broker_symbol.upper(), list(standard_symbols.keys()), n=1, cutoff=0.8)
    return matches[0] if matches else None

def connect_to_mt5(account: Account) -> bool:
    print(f"🔌 Connecting to {account.name} ({account.broker.name})")
    if not mt5.initialize(login=int(account.login), password=account.password, server=account.platform):
        print(f"❌ Connection failed: {mt5.last_error()}")
        return False
    return True

def sync_symbols_for_account(account: Account):
    if not connect_to_mt5(account):
        return

    symbols = mt5.symbols_get()
    print(f"📥 Retrieved {len(symbols)} symbols from {account.broker.name}")

    standard_symbols = {
        s.symbol.upper(): s for s in session.query(Symbol).all()
    }

    broker = account.broker

    for s in symbols:
        base_symbol = fuzzy_match_standard_symbol(s.name, standard_symbols)
        if not base_symbol:
            continue  # Skip unknown symbols

        std_sym = standard_symbols[base_symbol]

        # Check if symbol mapping already exists
        existing_mapping = session.query(SymbolMapping).filter_by(
            broker_id=broker.id,
            standard_symbol_id=std_sym.id,
            broker_symbol=s.name
        ).first()

        if not existing_mapping:
            mapping = SymbolMapping(
                broker_id=broker.id,
                standard_symbol_id=std_sym.id,
                broker_symbol=s.name,
                lot_size=s.trade_contract_size,
                leverage=100,  # You can customize this
                min_volume=s.volume_min,
                max_volume=s.volume_max,
                step_volume=s.volume_step,
                priority=1
            )
            session.add(mapping)
            session.commit()
            print(f"✅ Added mapping: {std_sym.symbol} -> {s.name}")
        else:
            mapping = existing_mapping

        # Add override if it doesn't exist
        override = session.query(AccountSymbolOverride).filter_by(
            account_id=account.id,
            symbol_mapping_id=mapping.id
        ).first()

        if not override:
            session.add(AccountSymbolOverride(
                account_id=account.id,
                symbol_mapping_id=mapping.id,
                is_active=True
            ))
            print(f"  ↪ Override added for account {account.login} -> {s.name}")

    session.commit()
    mt5.shutdown()
    print(f"✅ Finished syncing for {account.name}\n")

# ---------- Main Execution ----------

def main():
    accounts = session.query(Accounts).all()
    for account in accounts:
        sync_symbols_for_account(account)

if __name__ == "__main__":
    main()
