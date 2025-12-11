"""
Dashboard application for Armed Conflicts Analytics using Streamlit.
Includes page navigation and sidebar filters.
"""
import streamlit as st
import pandas as pd

# ---------------- Basic Configuration ----------------

# Configure the Streamlit page
st.set_page_config(
    page_title="Armed Conflicts Analytics Dashboard",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load data and store in session state
@st.cache_data
def load_data():
    return pd.read_csv('models/df_full_with_clusters.csv', index_col=0)
if "df" not in st.session_state:
    st.session_state['df'] = load_data()

df = st.session_state['df']

# Define pages for navigation
overview = st.Page("pages/01_overview.py",
                   title="Overview",
                   icon="🏠")
cluster_insights = st.Page("pages/02_cluster_insights.py",
                      title="Conflict Cluster Insights",
                      icon="❓")
pareto_modelling = st.Page("pages/03_paretor_modelling.py",
                      title="Pareto Modelling of Conflict Severity",
                      icon="❓")
conclusions = st.Page("pages/04_conclusions.py",
                      title="Conclusions",
                      icon="💡")

nav = st.navigation([overview, cluster_insights, pareto_modelling, conclusions])

current_page = nav.title

# ---------------- Sidebar (filters) ----------------
with st.sidebar:
    st.header("Filters")