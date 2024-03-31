import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

# ref: https://discuss.streamlit.io/t/new-login-page-navigation-example-with-streamlit-1-31/61529

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]

def make_menu():
    with st.sidebar:
        if st.session_state.get("logged_in", False):
            authenticated_menu()
        elif get_current_page_name() != "app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("app.py")
        

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.page_link("pages/home.py", label="Home", icon="🔍")
    st.page_link("pages/portfolio.py", label="Portfolio", icon="👤")
    if st.session_state.get("search_stock", None) is not None and st.session_state.search_stock != (None, None):
        st.sidebar.page_link("pages/symbol.py", label="Symbol", icon="📈")
    if st.session_state.role in ["admin"]:
        st.sidebar.page_link("pages/admin.py", label="admin", icon="🧑‍💻")
    if st.button("Log out"):
        logout()


def logout():
    st.session_state.role = None
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("app.py")

