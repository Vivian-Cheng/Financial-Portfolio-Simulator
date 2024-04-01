import streamlit as st
import requests
import pandas as pd
import altair as alt
from menu import make_menu

# Redirect to app.py if not logged in, otherwise show the navigation menu
make_menu()

# Verify the user's role
if st.session_state.role not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

if "realtime_db_stats" not in st.session_state:
    st.session_state.realtime_db_stats = None

def fetch_realtime_db_stat():
    res = requests.get('http://127.0.0.1:8080/realtime/dbstats')
    return res.json()
def refresh():
    st.session_state.realtime_db_stats = fetch_realtime_db_stat()
def run_realtime_commands(db, collection, action, query):
    params = {'db': db,
              'collection': collection,
              'action': action,
              'args': query}
    res = requests.get('http://127.0.0.1:8080/realtime/commands', params=params)
    return res.json()
def run_realtime_addnode():
    res = requests.get('http://127.0.0.1:8080/realtime/addnode')
    return res.json()
def run_realtime_deletenode():
    res = requests.get('http://127.0.0.1:8080/realtime/deletenode')
    return res.json()


st.title("Stock Quote real-time DB")
col_title, col_btn = st.columns([4, 1])
with col_title:
    st.markdown('''### DB Stats''')
with col_btn:
    if st.button("Refresh"):
        refresh()
tab_stats, tab_chart, tab_collection = st.tabs(["DB Stats", "Symbol Distributions", "Collections"])
st.session_state.realtime_db_stats = fetch_realtime_db_stat()
with tab_stats:
    realtime_db_stats_df = pd.DataFrame(st.session_state.realtime_db_stats['stats'])
    st.dataframe(realtime_db_stats_df, use_container_width=True)
    if st.button("Add Database"):
        with st.spinner('adding new database...'):
            res = run_realtime_addnode()
            st.write(res)
    if st.button("Remove Database"):
        with st.spinner('removing database...'):
            res = run_realtime_deletenode()
            st.write(res)
with tab_chart:
    chart_df = pd.DataFrame(st.session_state.realtime_db_stats['stats'])
    counts = pd.DataFrame({
        'database': chart_df.columns,
        'count': chart_df.loc['collections']
    })
    chart = alt.Chart(counts).mark_arc().encode(
        color='database',
        tooltip=['database', 'count'],
        angle='count'
    )
    st.altair_chart(chart, use_container_width=True)
with tab_collection:
    collections_df = pd.DataFrame(st.session_state.realtime_db_stats['collections']).T
    st.data_editor(
        collections_df,
        use_container_width=True
    )
    st.markdown('''#### Admin commands''')
    db = st.selectbox("Database", st.session_state.realtime_db_stats['collections'].keys())
    collection = st.selectbox("Collections", st.session_state.realtime_db_stats['collections'][db]['collections'])
    action = st.selectbox("Actions", 
                          ("drop","count","remove_expired", "drop_all"))
    query = ""
    if st.button("Run"):
        with st.spinner("running command..."):
            res = run_realtime_commands(db=db, collection=collection, action=action, query=query)
            st.write(res)

