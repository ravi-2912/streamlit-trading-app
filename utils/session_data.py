import numpy as np
import streamlit as st
import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import aliased

from models import Account, Broker, Instrument
from db.get_session import get_session
from utils.case_converter import snake_to_title


def load_instruments_to_session():
    if "instruments_df" not in st.session_state:
        with get_session() as session:
            instruments = session.query(Instrument).all()
            data = []
            for inst in instruments:
                data.append(
                    {
                        "ID": inst.id,
                        "Ticker": inst.ticker,
                        "Account ID": inst.account_id,
                        "Symbol ID": inst.symbol_id,
                        "Suffix ID": inst.suffix_id,
                    }
                )
            df = pd.DataFrame(data)
            try:
                df.set_index(
                    "ID",
                    inplace=True,
                )
            except KeyError:
                pass
            st.session_state["instruments_df"] = df


def load_accounts_to_session():
    if "accounts_df" not in st.session_state:
        with get_session() as session:
            data = []
            query = (
                session.query(
                    Account.id,
                    Account.name,
                    Account.login,
                    Account.type,
                    Account.platform,
                    Account.path,
                    Account.portable,
                    Account.server,
                    Account.currency,
                    Account.balance,
                    Broker.name.label("broker"),
                    func.count(Instrument.id).label("instrument_count")
                )
                .outerjoin(Broker, Account.broker_id == Broker.id)
                .outerjoin(Instrument, Instrument.account_id == Account.id)
                .group_by(Account.id, Broker.name)
            )
            accounts = query.all()
            for acc in accounts:
                data.append(
                    {
                        "ID": acc.id,
                        "Name": acc.name,
                        "Broker": acc.broker,
                        "Currency": acc.currency,
                        "Login": acc.login,
                        "Type": acc.type,
                        "Platform": acc.platform,
                        "Server": acc.server,
                        "Path": acc.path,
                        "Instruments #": acc.instrument_count,
                        "Balance": acc.balance
                    }
                )
            df = pd.DataFrame(data)
            try:
                df.set_index(
                    "ID",
                    inplace=True,
                )
            except KeyError:
                pass
            st.session_state["accounts_df"] = df


def get_all_items_from_table(table, fields) -> pd.DataFrame:
    with get_session() as session:
        items = session.query(table).all()
        data = []
        for item in items:
            data.append(
                {
                    **{snake_to_title(field) : getattr(item, field) for field in fields}
                }
            )
        df = pd.DataFrame(data)
        try:
            df.set_index(
                "ID",
                inplace=True,
            )
        except KeyError:
            pass
        return df
