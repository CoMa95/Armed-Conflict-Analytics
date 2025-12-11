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

<ul>

<li>
<u><b>1. Conflict activity is highly concentrated.</b></u><br>
A small number of clusters account for a disproportionately large share of recorded events, indicating that global conflict is driven by a few persistent hotspots.
</li>

<li>
<u><b>2. Organised state–rebel battles are the deadliest.</b></u><br>
Clusters dominated by battles between state forces and rebel groups show the highest average fatalities, reflecting the lethality of conventional armed confrontations.
</li>

<li>
<u><b>3. Violence against civilians forms its own conflict pattern.</b></u><br>
Several clusters are dominated by militia violence against civilians, characterised by high frequency but typically low fatalities per event.
</li>

<li>
<u><b>4. The same tactics behave differently depending on who uses them.</b></u><br>
Explosions and remote violence appear in multiple clusters, but their severity and frequency vary significantly depending on whether they are carried out by state or non-state actors.
</li>

<li>
<u><b>5. Regions exhibit distinct conflict “signatures.”</b></u><br>
Asia and the Middle East are dominated by state-rebel battles, Africa by militia-civilian violence, and Europe by remote or explosive attacks, highlighting strong regional patterns.
</li>

<li>
<u><b>6. Population density shapes conflict dynamics.</b></u><br>
Some clusters concentrate in dense urban areas, while others dominate sparsely populated regions, suggesting different forms of warfare in urban versus rural environments.
</li>

<li>
<u><b>7. Not all large conflict clusters are highly lethal.</b></u><br>
Several large clusters show very low average fatalities, indicating conflicts characterised by persistent low-level incidents rather than mass-casualty events.
</li>

</ul>

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