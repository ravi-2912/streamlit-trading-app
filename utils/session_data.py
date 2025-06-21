import streamlit as st
import pandas as pd
from db.get_session import get_session
from models.Accounts import Accounts

def load_accounts_to_session():
    if "accounts_df" not in st.session_state:
        with get_session() as session:
            accounts = session.query(Accounts).all()
            data = []
            for acc in accounts:
                data.append({
                    "ID": acc.id,
                    "Name": acc.name,
                    "Login": acc.login,
                    "Type": acc.type,
                    "Broker": acc.broker,
                    "Server": acc.server,
                })
            df = pd.DataFrame(data)
            try:
                df.set_index("ID", inplace=True,)
            except KeyError:
                pass
            st.session_state['accounts_df'] = df
