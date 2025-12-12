"""
Cluster Insights Page of the Armed Conflicts Analytics Dashboard.
Displays key performance indicators (KPIs) and visualisations based on filtered data.
"""

# import libraries
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- Page config ----------------
st.title("🔍 Conflict Cluster Insights")
st.markdown("Explore data-driven clusters of armed conflict events.")
st.markdown("---")
st.markdown("The clusters were generated using a semi-supervised method: DBSCAN was employed to create the cluster labels on a dataset sample, afterwards a k-NN was trained on the labelled sample and then predicted the labels for the rest of the dataset.")

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