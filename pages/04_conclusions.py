"""
Final Conclusions Page for Armed Conflict Analytics Dashboard
Provides a high-level summary of findings from clustering analysis and severity modelling."""

# import libraries
import streamlit as st

# ---------------- Page config ----------------
st.title("🧾 Conclusions")
st.markdown("A high-level summary of findings from the clustering analysis and severity modelling.")


# ---------------- Cluster Insights ----------------
st.markdown("""
<div style="padding: 18px; border-radius: 8px; background-color: #2b2b2b; color: #ffffff;">
<h3 style="color:#ffd700;">🔍 Cluster Insights — Summary</h3>

<p>
<i>Placeholder text — replace with your own layman explanation.</i>
</p>

<p>
Use this space to summarise the main insights from your DBSCAN clustering:
</p>

<ul>
<li>What kinds of patterns emerged?</li>
<li>How did clusters differ in geography, intensity, or actor types?</li>
<li>Which clusters represented large-scale organised conflict?</li>
<li>Which ones captured protests, militia skirmishes, or isolated events?</li>
<li>Did clusters reveal regional differences or structural similarities?</li>
</ul>

<p>
This box should help readers understand the <b>big picture</b> of the cluster results 
without requiring them to interpret the full analytics.
</p>

</div>
""", unsafe_allow_html=True)


st.markdown("---")


# ---------------- Pareto results ----------------
st.markdown("""
<div style="padding: 18px; border-radius: 8px; background-color: #2b2b2b; color: #ffffff;">
<h3 style="color:#ffd700;">📉 Pareto Severity Modelling — Summary</h3>

<p>
<i>Fitting the Pareto distribution to the dataset has revealed key insights about the nature of conflict severity:</i>
</p>

<ul>
<li>Conflict severity follows a heavy-tailed distribution, meaning most events cause few fatalities, but rare events cause extremely high casualties.</li>
<li>The fit is particularly strong past the 11+ fatalities count per individual event</li>
<li>It is however not perfect, mostly due to the natural contraints of conflicts (i.e. conflict severity cannot rise infinitely).</li>
</ul>

<p>
<b>Unfortunate practical implication:</b> "extreme violence is statistically expected rather than exceptional".
</p>

</div>
""", unsafe_allow_html=True)


st.markdown("---")


# ---------------- Authorship ----------------
st.caption("""
Dashboard created by Cosmin Manolescu  
Data Source: ACLED @ https://acleddata.com/  
Project: Armed Conflict Analytics
GitHub: https://github.com/CoMa95/Armed-Conflict-Analytics  
""")