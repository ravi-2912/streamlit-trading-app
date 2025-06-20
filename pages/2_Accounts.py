import streamlit as st
from models.Accounts import Accounts, SEVER_TYPE, ACOUNT_TYPE, ACCOUNT_FROM
from db.get_session import get_session
import pandas as pd
import threading

st.set_page_config(
    page_title="MT5 Account Manager",
    page_icon="📈",
    layout="wide"
)

st.title("Accounts")
st.write("Manage your accounts here.")

@st.cache_data(show_spinner=False)
def load_accounts():
    with get_session() as session:
        accounts = session.query(Accounts).all()
        data = []
        for acc in accounts:
            data.append({
                "Name": acc.name,
                "Login": acc.login,
                "Account Type": acc.type,
                "Broker": acc.account_from,
                "Server Type": acc.server_type,
                "API URL": acc.api_url,
                "API Port": acc.api_port,
            })
        return pd.DataFrame(data)


@st.dialog(title="Add Account", width="large")
def account_form():
    with st.form("account_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name")
        with col2:
            login = st.text_input("Login")
        password = st.text_input("Password", type="password")

        acc_type = st.selectbox("Account Type", ACOUNT_TYPE)
        broker = st.selectbox("Account From", ACCOUNT_FROM)
        server_type = st.selectbox("Server Type", SEVER_TYPE)


        submitted = st.form_submit_button("Submit")

        if submitted:
            with get_session() as session:
                new_account = Accounts(
                    name=name,
                    login=login,
                    _password=password,
                    type=acc_type,
                    broker=broker,
                    server_type=server_type,
                )
                session.add(new_account)

            st.success("Account added to database!")
            st.rerun()
        else: st.warning("Please fill out all fields.")


st.button("➕ Add Account", on_click=account_form)

with st.spinner("Loading accounts..."):
    accounts_df = load_accounts()
    st.dataframe(accounts_df, use_container_width=True)