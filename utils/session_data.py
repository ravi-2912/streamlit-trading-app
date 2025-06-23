import numpy as np
import streamlit as st
import pandas as pd
from db.get_session import get_session
from models import Account, Broker, Instrument

def load_instruments_to_session():
    if "instruments_df" not in st.session_state:
        with get_session() as session:
            instruments = session.query(Instrument).all()
            data = []
            for inst in instruments:
                data.append({
                    "ID": inst.id,
                    "Ticker": inst.ticker,
                    "Account ID": inst.account_id,
                    "Symbol ID": inst.symbol_id,
                    "Suffix ID": inst.suffix_id,
                })
            df = pd.DataFrame(data)
            try:
                df.set_index("ID", inplace=True,)
            except KeyError:
                pass
            st.session_state['instruments_df'] = df

def load_accounts_to_session(load_instruments: bool = True):
    if load_instruments:
        load_instruments_to_session()

    if "accounts_df" not in st.session_state:
        with get_session() as session:
            accounts = session.query(Account).all()
            instruments_df = st.session_state.get('instruments_df')
            data = []
            for acc in accounts:
                instruments = instruments_df[instruments_df["Account ID"] == acc.id]
                data.append({
                    "ID": acc.id,
                    "Name": acc.name,
                    "Login": acc.login,
                    "Type": acc.type,
                    "Platform": acc.platform,
                    "Server": acc.server,
                    "Path": acc.path,
                    "Instruments #": np.shape(instruments)[0],
                })
            df = pd.DataFrame(data)
            try:
                df.set_index("ID", inplace=True,)
            except KeyError:
                pass
            st.session_state['accounts_df'] = df

def load_brokers_to_session():
    if "brokers_df" not in st.session_state:
        with get_session() as session:
            brokers = session.query(Broker).all()
            data = []
            for acc in brokers:
                data.append({
                    "ID": acc.id,
                    "Name": acc.name,
                })
            df = pd.DataFrame(data)
            try:
                df.set_index("ID", inplace=True,)
            except KeyError:
                pass
            st.session_state['brokers_df'] = df