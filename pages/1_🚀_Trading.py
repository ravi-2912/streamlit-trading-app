from enum import Enum
import streamlit as st
import pandas as pd
from streamlit_tree_select import tree_select
from streamlit_quill import st_quill

from models.Account import AccountType, PlatformType
from models.Trade import DirectionType, OrderType
from models.currencies import CurrencyType
from utils.case_converter import title_to_snake
from utils.session_data import (
    load_accounts_to_session,
    load_brokers_to_session,
    load_symbols_to_session,
)
from utils.tree import build_tree

st.set_page_config(page_title="MT5 Trades Manager", page_icon="🚀", layout="wide")


def execute_trade():
    pass

st.title("🚀 Trading")
c1, c2,c3,c4,c5, c6 = st.columns(6)
c1.metric("Equity", 10000, "1%", border=True)
c2.metric("Available Margin", "95%", "-5%", border=True)
c3.metric("Active Position", "5", "5", border=True)
c4.metric("Active Orders", "5", "5", border=True)
c5.metric("Drawdown", "3%", "1%", border=True)
c6.metric("Daily Drawdown", "1%", "-0.5%", border=True)

st.divider()

st_col1, st_col2 = st.columns([1, 2], gap="large")

with st_col1:
    st.markdown("#### Accounts")
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

    options = list(enum_mapping.keys())
    grouping = st.multiselect(
        "Group accounts by (select one)",
        options=options,
        default=options[:2],
        help="Select how to group the accounts in the tree."
    )
    ungroup = list(set(options) - set(grouping))

    nodes, expanded = build_tree(st.session_state['accounts_df'], grouping, enum_mapping=enum_mapping, ungroup_keys=ungroup)
    selected = tree_select(nodes, show_expand_all=True, expanded=expanded)


with st_col2:
    st.markdown("#### Trade Parameters")
    c1, c2 = st.columns([3,1])
    strategy = c1.selectbox("Strategy", options=[], index=None, accept_new_options=True, placeholder="Select or write new strategy")
    trade_risk = 0.01 * c2.number_input("Trade Risk %", min_value=0.1, max_value=3.0, value=1.0, step=0.1, format="%.2f", help="Risk per trade per account")
    with st.expander("Common Parameters", expanded=True):
        c1, c2, c3, c4, c5 = st.columns(5)
        common_sl = c1.number_input("Stop Loss (pips)", step=1.0, min_value=5.0, value=15.0)
        common_tp = c2.number_input("Take Profit (pips)", step=1.0, min_value=5.0, value=15.0)
        common_dir = c3.selectbox("Direction", options=[direction.value for direction in DirectionType])
        common_order_type = c4.selectbox("Order Type", options=[order_type.value for order_type in OrderType])
        dir_currency = c5.selectbox("Direction based on Currency", options=["", *[currency.value for currency in CurrencyType]])

    symbols = st.multiselect("Select Symbols", options=st.session_state["symbols_df"]["Name"].tolist())
    if len(symbols) == 0 and "edited_df" in st.session_state:
        st.session_state.pop("edited_df")
    if symbols:
        if "edited_df" in st.session_state:
            df = st.session_state["edited_df"]
            current_symbols = set(symbols)
            existing_symbols = set(df["Symbol"])
            new_symbols = current_symbols - existing_symbols

            for symbol in new_symbols:
                df.loc[len(df)] = {
                    "Symbol": symbol,
                    "Risk %": trade_risk / len(symbols),
                    "Direction": common_dir,
                    "Order Type": common_order_type,
                    "Entry Price": None,
                    "SL/TP Factor": 1.0,
                    "SL Pips": common_sl,
                    "TP Pips": common_tp,
                    "Lots(~)": 0.1,
                    "Risk": 100.0
                }
            df = df[df["Symbol"].isin(symbols)].reset_index(drop=True)

        else:
            default_data = {
                "Symbol": symbols,
                "Risk %": [trade_risk/len(symbols)]*len(symbols),
                "Direction": [common_dir]*len(symbols),
                "Order Type": [common_order_type]*len(symbols),
                "Entry Price": [None]*len(symbols),
                "SL/TP Factor": [1.0]*len(symbols),
                "SL Pips": [common_sl]*len(symbols),
                "TP Pips": [common_tp]*len(symbols),
                "Lots(~)": [0.1]*len(symbols),
                "Risk": [100.0]*len(symbols),
            }
            df = pd.DataFrame(default_data)
            df["Symbol"] = symbols


        df["Risk %"] = [trade_risk/len(symbols)] * len(symbols)
        df["TP Pips"] = common_tp * df["SL/TP Factor"]
        df["SL Pips"] = common_sl * df["SL/TP Factor"]
        df["Order Type"] = [common_order_type] * len(symbols)

        def highlight_factor_cell(row):
            expected_sl = row["SL/TP Factor"] * common_sl
            expected_tp = row["SL/TP Factor"] * common_tp

            if round(row["SL Pips"], 2) != round(expected_sl, 2) or round(row["TP Pips"], 2) != round(expected_tp, 2):
                return ['background-color: red' if col == 'SL/TP Factor' else '' for col in row.index]
            else:
                return ['' for _ in row]
        df.style.apply(highlight_factor_cell, axis=1)

        edited_rows = st.session_state.get("updated_df", {}).get("edited_rows", {})
        for row_index, row_changes in edited_rows.items():
            factor = row_changes.get("SL/TP Factor", df.loc[row_index, "SL/TP Factor"])
            df.loc[row_index, "TP Pips"] = factor * common_tp
            df.loc[row_index, "SL Pips"] = factor * common_sl
            df.loc[row_index, "SL/TP Factor"] = factor

        st.session_state["edited_df"] = st.data_editor(
            df,
            key="updated_df",
            column_config={
                "Symbol": st.column_config.TextColumn("Symbol", disabled=True),
                "Risk %": st.column_config.NumberColumn("Risk %", format="percent"),
                "SL/TP Factor": st.column_config.NumberColumn("SL/TP Factor", default=1, help="Multiplier for Common SL/TP"),
                "Direction": st.column_config.SelectboxColumn("Direction", options=["Long", "Short"], required=True),
                "Order Type": st.column_config.SelectboxColumn("Order Type", options=["Market", "Limit", "Stop"], disabled=True),
                "Entry Price": st.column_config.NumberColumn("Entry Price", disabled=True if common_order_type == "Market" else False),
                "SL Pips": st.column_config.NumberColumn("SL Pips", default=common_sl, help="Override Common SL"),
                "TP Pips": st.column_config.NumberColumn("TP Pips", default=common_tp, help="Override Common TP"),
                "Lots(~)": st.column_config.NumberColumn("Lots", disabled=True),
                "Risk": st.column_config.NumberColumn("Risk", disabled=True),
            },
            use_container_width=True,
            num_rows="fixed",
        )
        st.button("Execute", on_click=execute_trade, icon=":material/rocket_launch:", )
        st.dataframe(st.session_state["edited_df"], use_container_width=True)

