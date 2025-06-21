import streamlit as st
from models.Accounts import Accounts, AccountType, BrokerType, ServerType
from db.get_session import get_session
import pandas as pd

from utils.session_data import load_accounts_to_session

st.set_page_config(
    page_title="Account Manager",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Accounts")


@st.dialog("Account Management", width="large")
def add_account():
    with st.form("account_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = col1.text_input("Name")
            login = st.text_input("Login")
            account_from = st.selectbox("Broker", [e.value for e in BrokerType])
        with col2:
            account_type = st.selectbox("Type", [e.value for e in AccountType])
            password = st.text_input("Password", type="password")
            server_type = st.selectbox("Server", [e.value for e in ServerType])

        submitted = st.form_submit_button("Submit")

        if submitted:
            with get_session() as session:
                new_account = Accounts(
                    name=name,
                    login=login,
                    password=password,
                    type=AccountType(account_type),
                    broker=BrokerType(account_from),
                    server=ServerType(server_type),
                )
                session.add(new_account)

            st.success("Account added to database!")
            st.session_state.pop("accounts_df", None)
            st.rerun()

st.button("Add Account", on_click=add_account)

with st.spinner("Loading accounts..."):
    if "accounts_df" not in st.session_state:
        load_accounts_to_session()
    st.dataframe(st.session_state['accounts_df'], use_container_width=True)
