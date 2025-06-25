import streamlit as st
from models.Account import Account, AccountType, PlatformType, CurrencyType
from db.get_session import get_session
import pandas as pd

from utils.session_data import load_accounts_to_session, load_brokers_to_session

st.set_page_config(page_title="Account Manager", page_icon="💼", layout="wide")

st.title("💼 Accounts")


@st.dialog("Account Management", width="large")
def add_account():
    with st.form("account_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = col1.text_input("Account Name")
        with col2:
            broker = st.selectbox(
                "Broker", st.session_state["brokers_df"]["Name"].tolist()
            )

        col1, col2 = st.columns(2)
        with col1:
            login = st.text_input("Login")
        with col2:
            password = st.text_input("Password", type="password")

        col1, col2 = st.columns(2)
        with col1:
            type = st.selectbox("Type", [e.value for e in AccountType])
        with col2:
            platform = st.selectbox("Platform", [e.value for e in PlatformType])

        col1, col2 = st.columns(2)
        with col1:
            path = st.text_input("Path")
        with col2:
            server = st.text_input("Server")

        c1, _ = st.columns(2)
        with c1:
            currency = st.selectbox("Currency", options=[currency.value for currency in CurrencyType])

        portable = st.checkbox("Portable", value=True)

        submitted = st.form_submit_button("Submit")
        broker_id = st.session_state["brokers_df"][
            st.session_state["brokers_df"]["Name"] == broker
        ].index[0]

        if submitted:
            with get_session() as session:
                new_account = Account(
                    name=name,
                    login=login,
                    password=password,
                    type=AccountType(type),
                    broker_id=broker_id,
                    platform=PlatformType(platform),
                    path=path,
                    portable=portable,
                    server=server,
                    currency=CurrencyType(currency),
                )
                session.add(new_account)

            st.success("Account added to database!")
            st.session_state.pop("accounts_df", None)
            st.rerun()


st.button("Add Account", on_click=add_account)

with st.spinner("Loading accounts..."):
    if "accounts_df" not in st.session_state:
        load_accounts_to_session()
    if "brokers_df" not in st.session_state:
        load_brokers_to_session()
    st.dataframe(st.session_state["accounts_df"], use_container_width=True)
