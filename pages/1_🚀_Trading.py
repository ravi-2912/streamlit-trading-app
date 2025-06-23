import streamlit as st
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

st_col1, st_col2 = st.columns([1, 3])

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

    with st_col1:
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

    with st_col2:
        symbols = st.multiselect(label="Asset", options=st.session_state["symbols_df"])
        with st.form("input_form"):
            input_data = {}

            for opt in symbols:
                st.markdown(f"###### {opt} Inputs")
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

                with col1:
                    text_val = st.text_input(f"{opt} Text", key=f"{opt}_text")
                with col2:
                    bool_val = st.checkbox(f"{opt} Bool", key=f"{opt}_bool")
                with col3:
                    num_val = st.number_input(f"{opt} Number", key=f"{opt}_number")
                # with col4:
                #     st.markdown(f"**{value_map[opt]}**")

                input_data[opt] = {
                    "text": text_val,
                    "bool": bool_val,
                    "number": num_val,
                    # "value": value_map[opt]
                }

            # Submit button
            submitted = st.form_submit_button("Execute")

        # Action on submit
        if submitted:
            st.success("Form submitted successfully!")
            st.write("Collected Input Data:")
            st.json(input_data)

# st.write(grouping)
# st.write(selected)
