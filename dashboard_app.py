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
    return pd.read_csv(
        "models/df_full_with_clusters.csv",
        index_col=0,
        parse_dates=["event_date"]
    )

df = load_data()

# compute top 15 clusters
cluster_counts = df["cluster"].value_counts().sort_values(ascending=False)
top_15_clusters = cluster_counts.index[:15].tolist()

# bin fatalities into categories
def categorize_fatalities(x):
    if x <= 3:
        return "Low (0-3)"
    elif x <= 10:
        return "Moderate (4-10)"
    elif x <= 50:
        return "High (11-50)"
    else:
        return "Extreme (50+)"
        
df["fatality_severity"] = df["fatalities"].apply(categorize_fatalities)

# ---------------- Page Navigation ----------------
overview = st.Page(
    "pages/01_overview.py",
    title="Overview",
    icon="🏠"
)

cluster_insights = st.Page(
    "pages/02_cluster_insights.py",
    title="Conflict Cluster Insights",
    icon="📊"
)

pareto_modelling = st.Page(
    "pages/03_pareto_modelling.py",   
    title="Pareto Modelling of Conflict Severity",
    icon="📉"
)

conclusions = st.Page(
    "pages/04_conclusions.py",
    title="Conclusions",
    icon="💡"
)

nav = st.navigation([overview, cluster_insights, pareto_modelling, conclusions])
current_page = nav.title

# ---------------- Sidebar (filters) ----------------
with st.sidebar:
    st.header("Filters")

    # Event type filter
    event_types = sorted(df["event_type"].dropna().unique())
    selected_event_types = st.multiselect(
        "Event Type",
        options=event_types,
        default=event_types
    )

    # Region filter
    regions = sorted(df["region"].dropna().unique())
    selected_regions = st.multiselect(
        "Region",
        options=regions,
        default=regions
    )

    # Cluster filter (top 15 most frequent)
    selected_clusters = st.multiselect(
        "Cluster (Top 15 by Size)",
        options=top_15_clusters,
        default=top_15_clusters
    )

    # Year range filter
    min_year = int(df["event_date"].dt.year.min())
    max_year = int(df["event_date"].dt.year.max())

    selected_years = st.slider(
        "Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    severity_levels = [
        "Low (0-3)",
        "Moderate (4-10)",
        "High (11-50)",
        "Extreme (50+)"
    ]

    selected_severity = st.multiselect(
        "Fatality Severity",
        options=severity_levels,
        default=severity_levels
    )


# ---------------- Apply Filters Through Function ----------------

def apply_filters(df_in: pd.DataFrame) -> pd.DataFrame:
    df_out = df_in.copy()

    if selected_event_types:
        df_out = df_out[df_out["event_type"].isin(selected_event_types)]

    if selected_regions:
        df_out = df_out[df_out["region"].isin(selected_regions)]

    if selected_clusters:
        df_out = df_out[df_out["cluster"].isin(selected_clusters)]
    
    if selected_severity:
        df_out = df_out[df_out["fatality_severity"].isin(selected_severity)]

    df_out = df_out[
        (df_out["event_date"].dt.year >= selected_years[0]) &
        (df_out["event_date"].dt.year <= selected_years[1])
    ]
    
    return df_out


# Save filtered df for all pages
st.session_state['filtered_df'] = apply_filters(df)

# Show number of events after filtering
st.sidebar.info(f"**Events after filtering: {st.session_state['filtered_df'].shape[0]}**")

# ---------------- Save global filters to session_state ----------------
st.session_state['global_filters'] = {
    "event_type": selected_event_types,
    "regions": selected_regions,
    "clusters": selected_clusters,
    'fatality_severity': selected_severity,
    "year_range": selected_years
}
# ---------------- Global Color Settings ----------------
severity_colors = {
    "Low (0-3)": "#91cfff",        # light blue
    "Moderate (4-10)": "#36a2eb",  # medium blue
    "High (11-50)": "#ff6384",     # red/pink
    "Extreme (50+)": "#8b0000"     # dark red
}

st.session_state["severity_colors"] = severity_colors

# Run the navigation
nav.run()