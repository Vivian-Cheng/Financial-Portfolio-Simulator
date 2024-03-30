import streamlit as st
from menu import make_menu

# Redirect to app.py if not logged in, otherwise show the navigation menu
make_menu()

# Verify the user's role
if st.session_state.role not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.title("This page is available to all admins")
st.markdown(f"You are currently logged with the role of {st.session_state.role}.")
