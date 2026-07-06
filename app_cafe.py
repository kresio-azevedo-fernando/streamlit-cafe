"""
Streamlit App — Coffee Shop Sales Optimisation
Seasonality + ABC Analysis · Live Interactive Demo
Author: Kresio Azevedo Fernando
Portfolio: kresio-azevedo-fernando.github.io
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(
    page_title="Coffee Shop Optimisation · Kresio Fernando",
    page_icon="☕",
    layout="wide",
)

st.markdown("""
<style>
body, .stApp { background-color: #09090f; color: #e8e8f0; }
.metric-card {
    background: #0f0f1a; border: 1px solid rgba(187,148,118,0.25);
    border-radius: 8px; padding: 1rem; text-align: center;
}
.metric-val { font-size: 1.8rem; font-weight: 700; color: #bb9476; }
.metric-lbl { font-size: 0.75rem; color: #9494a8; margin-top: 4px; }
h1, h2, h3 { color: #e8e8f0; }
.stButton > button {
    background: #bb9476; color: #000; font-weight: 700;
    border: none; border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

st.title("☕ Coffee Shop Sales Optimisation")
st.markdown(
    "**ABC Analysis + Seasonality Model** · "
    "[Portfolio](https://kresio-azevedo-fernando.github.io) · "
    "[Live Dashboard](https://app.powerbi.com/view?r=eyJrIjoiMDhjNjRiNjAtY2Y0MS00ZWE1LTk5ZTktNWM3NWIxM2M4MzZhIiwidCI6IjY1OWNlMmI4LTA3MTQtNDE5OC04YzM4LWRjOWI2MGFhYmI1NyJ9)"
)
st.markdown("---")

# ── REAL DATA ────────────────────────────────────────────────
PRODUCTS = {
    "Latte":               {"revenue": 26875.30, "qty": 757},
    "Americano with Milk": {"revenue": 24751.12, "qty": 809},
    "Cappuccino":          {"revenue": 17439.14, "qty": 486},
    "Americano":           {"revenue": 14650.26, "qty": 564},
    "Hot Chocolate":       {"revenue":  9933.46, "qty": 276},
    "Cocoa":               {"revenue":  8521.16, "qty": 239},
    "Cortado":             {"revenue":  7384.86, "qty": 287},
    "Espresso":            {"revenue":  2690.28, "qty": 129},
}

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTHLY_REV = [6398.86,13215.48,15891.64,5719.56,8164.42,
               7617.76,6915.94,7613.84,9988.64,13891.16,8590.54,8237.74]
MONTHLY_QTY = [201,423,494,168,241,223,237,272,344,426,259,259]

WEEKLY = {"Mon":17363,"Tue":18168,"Wed":15750,"Thu":16091,
          "Fri":16803,"Sat":14734,"Sun":13336}

TOTAL_REV = 112245.58
TOTAL_QTY = 3547

tab1, tab2, tab3 = st.tabs(["📊 KPIs & Products", "📅 Seasonality", "⚙️ Action Simulator"])

# ════════════════════════════════════════════════════════════
# TAB 1 — KPIs & ABC
# ════════════════════════════════════════════════════════════
with tab1:
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-val">€{TOTAL_REV:,.0f}</div><div class="metric-lbl">Annual Revenue</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{TOTAL_QTY:,}</div><div class="metric-lbl">Units Sold</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-val">€{max(MONTHLY_REV):,.0f}</div><div class="metric-lbl">Best Month (Mar)</div></div>', unsafe_allow_html=True)
    with c4:
        swing = (max(MONTHLY_REV)/min(MONTHLY_REV)-1)*100
        st.markdown(f'<div class="metric-card"><div class="metric-val">{swing:.0f}%</div><div class="metric-lbl">Revenue Swing</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Product Revenue — ABC Classification")

    df_prod = pd.DataFrame([
        {"Product": p, "Revenue": d["revenue"], "Units": d["qty"]}
        for p, d in PRODUCTS.items()
    ]).sort_values("Revenue", ascending=False)
    df_prod["Pct"] = (df_prod["Revenue"] / df_prod["Revenue"].sum() * 100).round(1)
    df_prod["Cumulative"] = df_prod["Pct"].cumsum()
    df_prod["Class"] = df_prod["Cumulative"].apply(
        lambda x: "A" if x <= 74 else "B" if x <= 90 else "C"
    )

    col1, col2 = st.columns([1,1])
    with col1:
        abc_colors = {"A":"#bb9476","B":"#6eb5ff","C":"#5a5a72"}
        fig, ax = plt.subplots(figsize=(6,4), facecolor="#09090f")
        ax.set_facecolor("#0f0f1a")
        bars = ax.barh(df_prod["Product"], df_prod["Revenue"],
                       color=[abc_colors[c] for c in df_prod["Class"]],
                       edgecolor="#1a1a28")
        for bar, pct in zip(bars, df_prod["Pct"]):
            ax.text(bar.get_width()+50, bar.get_y()+bar.get_height()/2,
                    f"{pct:.1f}%", va="center", fontsize=8, color="#9494a8")
        ax.tick_params(colors="#9494a8")
        ax.set_xlabel("Annual Revenue (€)", color="#9494a8")
        ax.set_title("Revenue by Product — ABC", color="#e8e8f0", fontsize=10)
        ax.legend(handles=[mpatches.Patch(color=abc_colors[c], label=f"Class {c}") for c in "ABC"],
                  facecolor="#141420", labelcolor="white", fontsize=7)
        for spine in ax.spines.values(): spine.set_color("#1a1a28")
        st.pyplot(fig); plt.close()

    with col2:
        st.dataframe(df_prod[["Product","Revenue","Units","Pct","Class"]].rename(
            columns={"Pct":"Rev %"}
        ), use_container_width=True, height=300)

        a_class = df_prod[df_prod["Class"]=="A"]
        st.info(f"**Class A:** {len(a_class)} products = {a_class['Pct'].sum():.0f}% of revenue\n\n"
                f"Products: {', '.join(a_class['Product'].tolist())}")

# ════════════════════════════════════════════════════════════
# TAB 2 — SEASONALITY
# ════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Monthly Revenue — Seasonality Analysis")

    mean_rev = np.mean(MONTHLY_REV)
    season_idx = [round(r/mean_rev, 3) for r in MONTHLY_REV]
    is_peak = [r >= mean_rev for r in MONTHLY_REV]

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(7,4), facecolor="#09090f")
        ax.set_facecolor("#0f0f1a")
        colors = ["#bb9476" if p else "#2d2d3a" for p in is_peak]
        bars = ax.bar(MONTHS, MONTHLY_REV, color=colors, edgecolor="#1a1a28")
        ax.axhline(mean_rev, color="#6eb5ff", linestyle="--", linewidth=1.5,
                   label=f"Avg €{mean_rev:,.0f}")
        for i, (bar, rev) in enumerate(zip(bars, MONTHLY_REV)):
            if is_peak[i]:
                ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+100,
                        f"€{rev/1000:.1f}K", ha="center", fontsize=7, color="#bb9476")
        ax.tick_params(colors="#9494a8")
        ax.set_ylabel("Revenue (€)", color="#9494a8")
        ax.set_title("Monthly Revenue — Peaks Highlighted", color="#e8e8f0", fontsize=10)
        ax.legend(facecolor="#141420", labelcolor="white", fontsize=8)
        for spine in ax.spines.values(): spine.set_color("#1a1a28")
        st.pyplot(fig); plt.close()

    with col2:
        fig, ax = plt.subplots(figsize=(7,4), facecolor="#09090f")
        ax.set_facecolor("#0f0f1a")
        idx_colors = ["#1D9E75" if x>=1.0 else "#ff6b6b" for x in season_idx]
        ax.bar(MONTHS, season_idx, color=idx_colors, edgecolor="#1a1a28")
        ax.axhline(1.0, color="white", linestyle="--", linewidth=1, label="Baseline")
        ax.tick_params(colors="#9494a8")
        ax.set_ylabel("Seasonality Index", color="#9494a8")
        ax.set_title("Seasonality Index per Month", color="#e8e8f0", fontsize=10)
        ax.legend(facecolor="#141420", labelcolor="white", fontsize=8)
        for spine in ax.spines.values(): spine.set_color("#1a1a28")
        st.pyplot(fig); plt.close()

    peak_months = [MONTHS[i] for i, p in enumerate(is_peak) if p]
    st.success(f"**Peak months:** {', '.join(peak_months)} — target promotions here for **+€8,400/year**")

    st.markdown("**Weekly Revenue Pattern**")
    weekly_df = pd.DataFrame(list(WEEKLY.items()), columns=["Day","Revenue"]).sort_values("Revenue", ascending=False)
    fig, ax = plt.subplots(figsize=(8,3), facecolor="#09090f")
    ax.set_facecolor("#0f0f1a")
    ax.bar(weekly_df["Day"], weekly_df["Revenue"], color="#bb9476", edgecolor="#1a1a28")
    ax.tick_params(colors="#9494a8")
    ax.set_ylabel("Annual Revenue (€)", color="#9494a8")
    ax.set_title("Revenue by Day of Week", color="#e8e8f0", fontsize=10)
    for spine in ax.spines.values(): spine.set_color("#1a1a28")
    st.pyplot(fig); plt.close()

# ════════════════════════════════════════════════════════════
# TAB 3 — ACTION SIMULATOR
# ════════════════════════════════════════════════════════════
with tab3:
    st.subheader("⚙️ Action Simulator — Adjust and see the impact")

    col1, col2 = st.columns([1,1])
    with col1:
        combo_uplift = st.slider("Combo ticket uplift (€/ticket)", 0.50, 3.00, 1.20, 0.10)
        peak_months_count = st.slider("Months with seasonal promotions", 1, 6, 3)
        staffing_gap = st.slider("Avg understaffed hours per day (peak days)", 0, 8, 4)
        avg_ticket   = st.number_input("Average ticket (€)", value=31.66, step=0.50)
        working_days = st.number_input("Working days/year", value=365, step=5)

    with col2:
        class_a_tickets  = sum(PRODUCTS[p]["qty"] for p in ["Latte","Americano with Milk","Cappuccino","Americano"])
        action1 = round(class_a_tickets * combo_uplift, 0)

        peak_rev_per_month = max(MONTHLY_REV)
        action3 = round(peak_months_count * peak_rev_per_month * 0.065, 0)

        hourly_rev   = TOTAL_REV / working_days / 8
        action2 = round(staffing_gap * hourly_rev * 120, 0)

        total_impact = action1 + action2 + action3
        pct_impact   = total_impact / TOTAL_REV * 100

        st.markdown("### 📊 Projected Annual Impact")
        r1,r2,r3 = st.columns(3)
        r1.metric("Menu Top 4 + Combos", f"+€{action1:,.0f}")
        r2.metric("Smart staffing", f"+€{action2:,.0f}")
        r3.metric("Seasonal promotions", f"+€{action3:,.0f}")

        st.markdown(f"""
        <div class="metric-card" style="margin-top:1rem;">
            <div class="metric-val">+€{total_impact:,.0f}</div>
            <div class="metric-lbl">Total annual opportunity = +{pct_impact:.1f}% over €{TOTAL_REV:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(6,3), facecolor="#09090f")
        ax.set_facecolor("#0f0f1a")
        actions = ["Menu+Combos","Smart Staffing","Seasonal Promo"]
        values  = [action1, action2, action3]
        colors  = ["#bb9476","#6eb5ff","#1D9E75"]
        bars = ax.bar(actions, values, color=colors, edgecolor="#1a1a28")
        for bar, val in zip(bars, values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+200,
                    f"+€{val:,.0f}", ha="center", fontsize=9,
                    color="white", fontweight="bold")
        ax.tick_params(colors="#9494a8")
        ax.set_ylabel("Annual Impact (€)", color="#9494a8")
        ax.set_title("3 Actions — Projected Impact", color="#e8e8f0", fontsize=10)
        for spine in ax.spines.values(): spine.set_color("#1a1a28")
        st.pyplot(fig); plt.close()

st.markdown("---")
st.markdown(
    "**Kresio Azevedo Fernando** · BI & Decision Optimisation Specialist · "
    "[kresio-azevedo-fernando.github.io](https://kresio-azevedo-fernando.github.io)"
)
