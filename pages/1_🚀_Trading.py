import streamlit as st
from streamlit_tree_select import tree_select

from models.Account import BrokerType, AccountType, PlatformType
from utils.case_converter import pascal_to_title
from utils.session_data import load_accounts_to_session, load_brokers_to_session
from utils.tree import build_tree

st.set_page_config(
    page_title="MT5 Trades Manager",
    page_icon="🚀",
    layout="wide"
)


st.title("🚀 Trading")

st_col1, st_col2 = st.columns([1, 3])

# enum_mapping = {
#     "Type": AccountType,
#     "Broker": BrokerType,
#     "Platform": PlatformType
# }

# with st.spinner("Loading accounts..."):
#     if "accounts_df" not in st.session_state:
#         load_accounts_to_session()
#     if "brokers_df" not in st.session_state:
#         load_brokers_to_session()

#     with st_col1:
#         st.text("Select account(s) from the tree below:")
#         options = list(enum_mapping.keys())
#         grouping = st.multiselect(
#             "Group accounts by (select one)",
#             options=options,
#             default=options[:2],
#             help="Select how to group the accounts in the tree."
#         )
#         ungroup = list(set(options) - set(grouping))

#         nodes = build_tree(st.session_state['accounts_df'], grouping, enum_mapping=enum_mapping, ungroup_keys=ungroup)
#         selected = tree_select(nodes, show_expand_all=True)

        # st.write(grouping)
        # st.write(selected)

