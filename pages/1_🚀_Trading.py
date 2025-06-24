from enum import Enum
import streamlit as st
import pandas as pd
from streamlit_tree_select import tree_select
from streamlit_quill import st_quill

from models.Account import AccountType, PlatformType
from utils.case_converter import title_to_snake
from utils.session_data import (
    load_accounts_to_session,
    load_brokers_to_session,
    load_symbols_to_session,
)
from utils.tree import build_tree

st.set_page_config(page_title="MT5 Trades Manager", page_icon="🚀", layout="wide")


st.title("🚀 Trading")

st_col1, st_col2 = st.columns([1, 2], gap="large")

with st.spinner("Loading accounts..."):
    if "accounts_df" not in st.session_state:
        load_accounts_to_session()
    if "brokers_df" not in st.session_state:
        load_brokers_to_session()
    if "symbols_df" not in st.session_state:
        load_symbols_to_session()

    enum_mapping = {
        "Type": AccountType,
        "Broker": Enum("BrokerType", {title_to_snake(item): item for item in st.session_state["brokers_df"]["Name"].tolist()}, type=str),
        "Platform": PlatformType
    }

with st_col1:
    st.text("Select account(s) from the tree below:")
    options = list(enum_mapping.keys())
    grouping = st.multiselect(
        "Group accounts by (select one)",
        options=options,
        default=options[:2],
        help="Select how to group the accounts in the tree."
    )
    ungroup = list(set(options) - set(grouping))

    nodes, expansions = build_tree(st.session_state['accounts_df'], grouping, enum_mapping=enum_mapping, ungroup_keys=ungroup)
    selected = tree_select(nodes, show_expand_all=True, )

with st_col2:
    st.selectbox("Strategy", options=[], index=None, accept_new_options=True, placeholder="Select or write new strategy")
    st.number_input("Trade Risk %", min_value=0.125, max_value=2.5, value=0.5, step=0.125)
    with st.expander("Common Parameters", expanded=True):
        c1, c2, c3, c4, = st.columns(4)
        c1.number_input("Stop Loss (pips)", step=1, min_value=5, value=15)
        c2.number_input("Take Profit (pips)", step=1, min_value=5, value=15)
        c3.selectbox("Direction", options=["Long", "Short"])
        c4.selectbox("Order Type", options=["Market", "Limit", "Stop"])
        c1, c2, c3, c4 = st.columns(4)
        c1.selectbox("Direction based on Currency", options=["", "USD", "GBP"])

    symbols = st.multiselect(
        "Select Symbols",
        options=st.session_state["symbols_df"]["Name"].tolist(),

    )
    if symbols:
        default_data = {
            "Symbol": [],
            "Risk %": [],
            "SL/TP Factor": [],
            "Direction": [],
            "Order Type": [],
            "Entry Price": [],
            "SL Price": [],
            "TP Price": [],
            "Lots": [],
            "Risk": [],
        }
        df = pd.DataFrame(default_data)
        df["Symbol"] = symbols

        edited_df = st.data_editor(
            df,
            column_config={
                "Symbol": st.column_config.TextColumn("Symbol", disabled=True),
                "Risk %": st.column_config.NumberColumn("Risk"),
                "SL/TP Factor": st.column_config.NumberColumn("SL/TP Factor"),
                "Direction": st.column_config.SelectboxColumn("Direction", options=["Long", "Short"]),
                "Order Type": st.column_config.SelectboxColumn("Order Type", options=["Market", "Limit", "Stop"]),
                "Entry Price": st.column_config.NumberColumn("Entry Price"),
                "SL Price": st.column_config.NumberColumn("SL Price"),
                "TP Price": st.column_config.NumberColumn("TP Price"),
                "Lots": st.column_config.NumberColumn("Lots", disabled=True),
                "Risk": st.column_config.NumberColumn("Risk", disabled=True),
            },
            use_container_width=True,
            num_rows="fixed",
        )

        notes = st_quill(placeholder="Notes")
    # if st.button("Execute"):
    #     st.success("Inputs submitted!")
    #     st.write("Processed Data:")
        # st.rerun()

