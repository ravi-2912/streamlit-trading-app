import streamlit as st
import pandas as pd
from db.get_session import get_session
from models.Account import Account

def get_all_accounts() -> pd.DataFrame:
    if "accounts_df" not in st.session_state:
        with get_session() as session:
            accounts = session.query(Account).all()
            data = []
            for acc in accounts:
                data.append({
                    "ID": acc.id,
                    "Name": acc.name,
                    "Login": acc.login,
                    "Type": acc.type,
                    "Broker": acc.broker,
                    "Server": acc.platform,
                })
            df = pd.DataFrame(data)
            try:
                df.set_index("ID", inplace=True,)
            except KeyError:
                pass
            return df
