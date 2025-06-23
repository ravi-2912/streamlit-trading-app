import streamlit as st
import pandas as pd
from streamlit_tree_select import tree_select

from models.Account import AccountType, PlatformType
from utils.case_converter import pascal_to_title
from utils.session_data import (
    load_accounts_to_session,
    load_brokers_to_session,
    load_symbols_to_session,
)
from utils.tree import build_tree

st.set_page_config(page_title="MT5 Trades Manager", page_icon="🚀", layout="wide")


st.title("🚀 Trading")

# enum_mapping = {
#     "Type": AccountType,
#     "Broker": BrokerType,
#     "Platform": PlatformType
# }

with st.spinner("Loading accounts..."):
    if "accounts_df" not in st.session_state:
        load_accounts_to_session()
    if "brokers_df" not in st.session_state:
        load_brokers_to_session()
    if "symbols_df" not in st.session_state:
        load_symbols_to_session()

    st.text("Select account(s) from the tree below:")
    # options = list(enum_mapping.keys())
    # grouping = st.multiselect(
    #     "Group accounts by (select one)",
    #     options=options,
    #     default=options[:2],
    #     help="Select how to group the accounts in the tree."
    # )
    # ungroup = list(set(options) - set(grouping))

    # nodes = build_tree(st.session_state['accounts_df'], grouping, enum_mapping=enum_mapping, ungroup_keys=ungroup)
    # selected = tree_select(nodes, show_expand_all=True)

    symbols = st.multiselect(label="Asset", options=st.session_state["symbols_df"])
    if symbols:
        # Prefill the DataFrame
        default_data = {
            "Option": symbols,
            "Text": [""] * len(symbols),
            "Bool": [False] * len(symbols),
            "Number": [0] * len(symbols),
            # "Value": [value_map[opt] for opt in selected_options]
        }
        df = pd.DataFrame(default_data)

        # Let user edit text, bool, number (not 'Value' or 'Option')
        edited_df = st.data_editor(
            df,
            column_config={
                "Text": st.column_config.TextColumn("Text Input"),
                "Bool": st.column_config.CheckboxColumn("Boolean"),
                "Number": st.column_config.NumberColumn("Number Input"),
                "Value": st.column_config.TextColumn(
                    "Value (readonly)", disabled=True
                ),
                "Option": st.column_config.TextColumn("Option", disabled=True),
            },
            use_container_width=True,
            num_rows="fixed",
        )

        # Submit button
        if st.button("Execute"):
            st.success("Inputs submitted!")
            st.write("Processed Data:")
            st.dataframe(edited_df)


# st.write(grouping)
# st.write(selected)
