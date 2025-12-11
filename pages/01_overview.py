"""
Overview Page of the Armed Conflicts Analytics Dashboard.
Displays key performance indicators (KPIs) and visualisations based on filtered data.
"""

# import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- Page config ----------------
st.title("🌍 Armed Conflict Overview")
st.markdown("This page provides a high-level snapshot of the filtered conflict dataset.")


# ---------------- Load filtered data ----------------
if "filtered_df" not in st.session_state:
    st.warning("No data found. Please visit the Home page to load and filter the dataset.")
    st.stop()

df = st.session_state["filtered_df"]
severity_colors = st.session_state["severity_colors"]

# --------------- KPI Cards ---------------
st.subheader("Key Metrics")

total_events = df.shape[0]
total_fatalities = int(df["fatalities"].sum())
avg_fatalities = df["fatalities"].mean()
num_clusters = df["cluster"].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Events", f"{total_events:,}")
col2.metric("Total Fatalities", f"{total_fatalities:,}")
col3.metric("Avg Fatalities per Event", f"{avg_fatalities:.2f}")
col4.metric("Clusters Represented", num_clusters)


# --------------- Tabs Section ---------------
static_tab, dynamic_tab = st.tabs(["📸 Static Showcase", "⚡ Dynamic Interactive Charts"])


# --------------- STATIC SHOWCASE TAB ---------------
with static_tab:
    st.subheader("Spatial Distribution of Conflict Events")
    st.image("figures/geo_kde.png", use_container_width=True)

    st.subheader("Temporal Severity of Conflict Events")
    st.image("figures/temporal_plot.png", use_container_width=True)

# --------------- DYNAMIC INTERACTIVE TAB ---------------
with dynamic_tab:

    # ---- Interactive Visual 1: Events Over Time ----
    st.subheader("📈 Events Over Time")

    if "event_date" not in df.columns:
        st.error("event_date column missing from dataframe!")
    else:
        df_time = df.copy()
        df_time["year"] = df_time["event_date"].dt.year
        events_per_year = df_time.groupby("year").size()

        st.line_chart(events_per_year)

    # ---- Interactive Visual 2: Severity Distribution ----
    st.subheader("🔥 Fatality Severity Distribution")

    severity_counts = (
        df["fatality_severity"]
        .value_counts()
        .reindex(severity_colors.keys(), fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(
        severity_counts.index,
        severity_counts.values,
        color=[severity_colors[s] for s in severity_counts.index]
    )

    ax.set_xlabel("Severity Category")
    ax.set_ylabel("Event Count")
    ax.set_title("Fatality Severity Breakdown")

    plt.xticks(rotation=20)
    st.pyplot(fig)


# --------------- Footer ---------------
st.markdown("---")
st.caption("Data filtered using global sidebar selections.")