"""
Pareto Modelling Page of the Armed Conflicts Analytics Dashboard.
Displays key performance indicators (KPIs) and visualisations based on filtered data.
"""

# import libraries
import streamlit as st
import pandas as pd

# ---------------- Page config ----------------
st.title("📉 Pareto Modelling of Conflict Severity")

st.markdown("""
### Power-Law / Pareto Severity Analysis

**Why fitting a Pareto/Power Law model?**

Conflict fatalities are not distributed normally: most events cause few deaths, while a small number cause extremely high casualties. A power-law (Pareto) distribution may capture this imbalance by modeling how ***rare, catastrophic events dominate the overall dynamics of violence***.

Confirming whether fatalities follow the power-law is important because:
1. It reveals the risk structure of violent conflict
2. Identifies scale-free dynamics, i.e. if severe conflicts follow the power law, then the same mechanisms may apply accross scales (e.g. skirmishes, major battles, regional wars)
3. May guide further modelling and scenario planning

**In Short:** Conflict fatalities follow a heavy-tailed distribution, meaning rare, extreme events play a disproportionate role; modeling this with a Pareto/power-law distribution helps explain the underlying structure and risk profile of violent conflict.

---
""")

# ---------------- CCDF Curve ----------------
st.subheader("Empirical CCDF vs Fitted Power-Law Model")

st.image("figures/cluster_ccdf_powerlaw.png", use_container_width=True)

st.markdown("""
**Explanation of lines:**

- **Empirical CCDF (blue line):**  
  Shows the observed probability that an event has fatalities ≥ x.  
  This is the true severity tail of the conflict dataset.

- **Power-law fit (red dashed line):**  
  The theoretical model fitted to the tail (x ≥ xmin).  
  Used to estimate α and assess whether the distribution follows a heavy-tailed pattern.
""")

st.markdown("---")

# ---------------- Pareto Fit KPIs ----------------
st.subheader("Model Fit Summary")

# define results
alpha = 2.55
xmin = 11
R_logn = -168.5
p_logn = '< 0.00...'
R_exp = 3739.7
p_exp = '< 0.00...'

# organise KPIs in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Pareto Parameters")
    st.metric("α (Alpha)", f"{alpha:.2f}")
    st.metric("xmin", xmin)

with col2:
    st.markdown("### Lognormal Comparison")
    st.metric("R (PL vs Lognormal)", f"{R_logn:.2f}")
    st.metric("p-value", p_logn)

with col3:
    st.markdown("### Exponential Comparison")
    st.metric("R (PL vs Exponential)", f"{R_exp:.2f}")
    st.metric("p-value", p_exp)

st.markdown("---")

# ---------------- Interpretation ----------------
st.subheader("Interpretation of Results")

st.markdown("""
1. α = 2.55 implies:
    - Moderately heavy-tailed distribution, i.e. extreme events are rare but systematically present
    - Tail decays slower than true exponential, but faster than very heavy tails

2. xmin = 11 fatalities:
    - Power-law behaviour holds only for events with **11+ fatalities**
    - Below the threshold there is a different distribution type
            
3. CCDF tapers off towards the end:
    - The Power-Law extropolates, but the real data cannot sustain infinite tails as real life events have natural constraints (population, geography etc.) 
    - Also, there are far fewer observations towards the higher fatalities end, becoming increasingly noisier
    - So for the most catastrophic events, fatalities deviate from a pure Power-Law

4. Versus Lognormal R = -168.6 and p < 0.00... implies:
    - Lognormal fits significantly better than power law in this case
    - Coroborates with xmin = 11 => overall, fatalities show heavy-tailed behaviour consistent with power-law scaling, but the lognormal distribution provides a significantly better fit to the observed tail due to the non-power law behaviour of the tail's end

5. Versus Exponential R = 3739.7 and p < 0.00... implies:
    - Power-Law fits significantly better than the exponential
    - This is mostly due to the slower-than-exponential decay of tail => extreme fatalities events are far more common than an exponential model would predict
""")