"""
Cluster Insights Page of the Armed Conflicts Analytics Dashboard.
Displays key performance indicators (KPIs) and visualisations based on filtered data.
"""

# import libraries
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# ---------------- Page config ----------------
st.title("🔍 Conflict Cluster Insights")
st.markdown("Explore data-driven clusters of armed conflict events.")


# ---------------- Load filtered data ----------------
df = st.session_state["filtered_df"]
severity_colors = st.session_state["severity_colors"]


# --------------- Tabs Section ---------------
static_tab, dynamic_tab, profile_tab = st.tabs(
    ["📸 Static", "⚡ Dynamic", "🧬 Cluster Profile"]
)


# --------------- Tab 1 ---------------
with static_tab:
    st.subheader("Total Fatalities per Cluster")
    st.image("figures/cluster_fatalities.png", use_container_width=True)

    st.subheader("Cluster Fatalities vs Population Density")
    st.image("figures/cluster_pop_density.png", use_container_width=True)

# --------------- Tab 2 ---------------
with dynamic_tab:

    # temporal activity with altair
    st.subheader("📈 Temporal Activity of Selected Clusters")

    top_clusters = st.session_state["top_15_clusters"]

    df_time = df.copy()
    df_time["year"] = df_time["event_date"].dt.year

    # Only include top clusters
    df_time = df_time[df_time["cluster"].isin(top_clusters)]

    cluster_year_counts = (
        df_time.groupby(["cluster", "year"])
        .size()
        .reset_index(name="events")
    )

    chart = (
        alt.Chart(cluster_year_counts)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("events:Q", title="Event Count"),
            color=alt.Color("cluster:N", title="Cluster"),
            tooltip=["cluster:N", "year:O", "events:Q"],
        )
        .properties(height=350)
    )

    st.altair_chart(chart, use_container_width=True)

    # spatial density heatmap with altair
    st.subheader("🌍 Spatial Density of Selected Clusters")
    st.markdown("**Note:** Select fewer clusters for better performance.")
    df_map = df.copy()

    # Prepare list of [lat, lon] pairs
    heat_data = df_map[["latitude", "longitude"]].dropna().values.tolist()

    # Center map on mean location
    center_lat = df_map["latitude"].mean()
    center_lon = df_map["longitude"].mean()

    # Create base map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=2, tiles="cartodbpositron")

    # Add heatmap layer
    HeatMap(
        heat_data,
        radius=8,        # controls smoothing — higher = smoother
        blur=15,         # further smoothness
        max_zoom=4,
    ).add_to(m)

    # Display in Streamlit
    st_folium(m, width=900, height=550)


# --------------- Tab 3 ---------------
with profile_tab:

    st.subheader("Select a Cluster for Detailed Profile")

    # Only allow clusters that actually appear after filtering
    top_clusters = st.session_state["top_15_clusters"]
    available_clusters = [c for c in top_clusters if c in df["cluster"].unique()]

    selected_cluster = st.selectbox(
        "Choose a Cluster",
        options=available_clusters,
        index=0
    )

    df_cluster = df[df["cluster"] == selected_cluster]

    st.markdown(f"### Cluster {selected_cluster} Summary")

    # Build summary table
    summary = {
        "ID": int(selected_cluster),
        "No. of Events": df_cluster.shape[0],
        "Mean fatalities": round(df_cluster["fatalities"].mean(), 2),
        "Median fatalities": round(df_cluster["fatalities"].median(), 2),
        "Dominant Event": df_cluster["event_type"].mode()[0],
        "Dom. Sub Event": df_cluster["sub_event_type"].mode()[0],
        "Dom. Interaction": df_cluster["interaction"].mode()[0],
        "Dom. Region": df_cluster["region"].mode()[0],
        "Dom. Country": df_cluster["country"].mode()[0],
        "Median Pop. density": int(df_cluster["population_best"].median()),
        "Earliest event": df_cluster["event_date"].min().strftime("%Y-%m-%d"),
        "Latest event": df_cluster["event_date"].max().strftime("%Y-%m-%d"),
    }

    st.table(pd.DataFrame(summary, index=[0]))

    # cluster temporal pattern
    st.markdown("#### Temporal Pattern")

    df_time_c = df_cluster.copy()
    df_time_c["year"] = df_time_c["event_date"].dt.year

    events_year = (
        df_time_c.groupby("year").size().reset_index(name="events")
    )

    line = (
        alt.Chart(events_year)
        .mark_line(point=True, color="steelblue")
        .encode(
            x="year:O",
            y="events:Q"
        )
    )

    st.altair_chart(line, use_container_width=True)


    # cluster severity distribution
    st.markdown("#### Fatality Severity Breakdown")

    sev_counts = (
        df_cluster["fatality_severity"]
        .value_counts()
        .reindex(severity_colors.keys(), fill_value=0)
        .reset_index()
    )
    sev_counts.columns = ["severity", "count"]

    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(
        sev_counts["severity"],
        sev_counts["count"],
        color=[severity_colors[s] for s in sev_counts["severity"]]
    )
    plt.xticks(rotation=20)
    st.pyplot(fig)