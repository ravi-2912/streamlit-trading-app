import streamlit as st

from models import Broker, Account, AccountType, PlatformType, CurrencyType
from db.get_session import get_session

from utils.session_data import get_all_items_from_table, get_all_items_from_account

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
            currency = st.selectbox(
                "Currency", options=[currency.value for currency in CurrencyType]
            )

        portable = st.checkbox("Portable", value=True)

        submitted = st.form_submit_button("Submit")
        broker_id = st.session_state["brokers_df"][st.session_state["brokers_df"]["Name"] == broker].index[0]

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


c1,c2, _= st.columns([1,1,7])
c1.button("Add Account", icon="➕", on_click=add_account)
archive = c2.button("🗄️ Archive")



with st.spinner("Loading accounts..."):
    if "accounts_df" not in st.session_state:
        st.session_state["accounts_df"] = get_all_items_from_account()
    if "brokers_df" not in st.session_state:
        st.session_state["brokers_df"] = get_all_items_from_table(
            Broker, ["id", "name"]
        )
    original_df = st.session_state["accounts_df"]

    edited_df = st.data_editor(
        original_df[original_df["Archived"] == False],
        use_container_width=True,
        num_rows="fixed",
        key="updates_on_df",
        column_config={
            "ID": st.column_config.NumberColumn("ID", disabled=True),
            "Name": st.column_config.TextColumn("Name", ),
            "Broker": st.column_config.TextColumn("Broker", disabled=True),
            "Login": st.column_config.TextColumn("Login", disabled=True),
            "Type": st.column_config.TextColumn("Type", disabled=True),
            "Platform": st.column_config.TextColumn("Platform", disabled=True),
            "Path": st.column_config.TextColumn("Path",),
            "Portable": st.column_config.CheckboxColumn("Portable", disabled=True),
            "Server": st.column_config.TextColumn("Server", ),
            "Currency": st.column_config.TextColumn("Currency", disabled=True),
            "Balance": st.column_config.NumberColumn("Balance", disabled=True),
            "Instruments #":st.column_config.NumberColumn("Instruments #", disabled=True),
            "Archive": st.column_config.CheckboxColumn("Archive", disabled=False, help="Mark for archiving"),
        })

    removed_ids = edited_df[edited_df["Archived"] == True].index.tolist()

    if len(removed_ids):
        st.warning(f"{len(removed_ids)} account(s) marked for archiving.")
        if archive:
            with get_session() as session:
                session.query(Account).filter(Account.id.in_(removed_ids)).update(
                    {Account.archived: True}, synchronize_session=False
                )
            session.commit()
            st.success(f"Archived {len(removed_ids)} account(s).")
            st.session_state.pop("accounts_df", None)
            st.rerun()

# TODO: Implement multi row edit and commit to DB
# TODO: Implement show Account Balance curve (all) including All Accounts, filterable
