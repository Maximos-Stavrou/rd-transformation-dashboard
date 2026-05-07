"""
app.py — R&D Digital Transformation ROI Dashboard
Author: Maximos Stavrou

A portfolio project demonstrating how Life Sciences and CPG companies can
measure and visualize the ROI of digital transformation initiatives in R&D.

Built with: Streamlit, Plotly, Pandas, and Claude (Anthropic) for GenAI insights.

To run locally:
    pip install -r requirements.txt
    streamlit run app.py
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import anthropic
import json

from data import (
    get_experiment_data,
    get_cost_savings_data,
    get_eln_adoption_data,
    get_kpi_summary,
    QUARTERS,
    PRODUCT_LINES,
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="R&D Digital Transformation Dashboard",
    page_icon="🔬",
    layout="wide",
)

# ─────────────────────────────────────────────
# CUSTOM STYLING
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #F8F9FA; }
    .kpi-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #1F4E79;
    }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #1F4E79; }
    .kpi-label { font-size: 0.85rem; color: #666; margin-top: 4px; }
    .phase-badge-pre {
        background: #FFE8E8; color: #C0392B;
        padding: 2px 10px; border-radius: 12px; font-size: 0.8rem;
    }
    .phase-badge-post {
        background: #E8F5E9; color: #1B5E20;
        padding: 2px 10px; border-radius: 12px; font-size: 0.8rem;
    }
    .insight-box {
        background: #EEF4FB;
        border-left: 4px solid #2E75B6;
        border-radius: 6px;
        padding: 16px 20px;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("## 🔬 R&D Digital Transformation ROI Dashboard")
st.markdown(
    "Tracking the operational and financial impact of digital transformation initiatives "
    "across R&D workflows in CPG & Life Sciences. "
    "<span class='phase-badge-pre'>Pre-Digital: Q1–Q2 2023</span>&nbsp;"
    "<span class='phase-badge-post'>Post-Digital: Q3 2023 onward</span>",
    unsafe_allow_html=True
)
st.divider()

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
exp_df = get_experiment_data()
cost_df = get_cost_savings_data()
adoption_df = get_eln_adoption_data()
kpis = get_kpi_summary()

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-value'>{kpis['cycle_time_reduction']}</div>
        <div class='kpi-label'>⏱ Reduction in Experiment Cycle Time</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-value'>{kpis['total_savings']}</div>
        <div class='kpi-label'>💰 Total Cost Savings (Post-Digital)</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-value'>{kpis['eln_adoption']}</div>
        <div class='kpi-label'>📋 Avg ELN Adoption Rate (Q4 2024)</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-value'>{kpis['experiments_run']}</div>
        <div class='kpi-label'>🧪 Total Experiments Tracked</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTERS
# ─────────────────────────────────────────────
with st.expander("🔧 Filters", expanded=False):
    selected_products = st.multiselect(
        "Product Lines", PRODUCT_LINES, default=PRODUCT_LINES
    )
    selected_quarters = st.multiselect(
        "Quarters", QUARTERS, default=QUARTERS
    )

# Apply filters
filtered_exp = exp_df[
    (exp_df["Product Line"].isin(selected_products)) &
    (exp_df["Quarter"].isin(selected_quarters))
]
filtered_cost = cost_df[
    (cost_df["Product Line"].isin(selected_products)) &
    (cost_df["Quarter"].isin(selected_quarters))
]

# ─────────────────────────────────────────────
# CHARTS — ROW 1
# ─────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("#### ⏱ Experiment Cycle Time by Product Line")
    fig1 = px.line(
        filtered_exp,
        x="Quarter", y="Avg Cycle Time (Days)",
        color="Product Line",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    # Add vertical line at digital transformation cutoff
    fig1.add_vline(
        x=2, line_dash="dash", line_color="#C0392B",
        annotation_text="Digital Rollout", annotation_position="top right"
    )
    fig1.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),
        margin=dict(t=20, b=10),
        yaxis_title="Avg Days",
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.markdown("#### 💰 Cumulative Cost Savings by Product Line")
    fig2 = px.area(
        filtered_cost,
        x="Quarter", y="Cumulative Savings ($)",
        color="Product Line",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig2.add_vline(
        x=2, line_dash="dash", line_color="#C0392B",
        annotation_text="Digital Rollout", annotation_position="top right"
    )
    fig2.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),
        margin=dict(t=20, b=10),
        yaxis_title="Cumulative Savings (USD)",
    )
    st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────
# CHARTS — ROW 2
# ─────────────────────────────────────────────
col_c, col_d = st.columns(2)

with col_c:
    st.markdown("#### 📋 ELN Adoption Rate by Team")
    fig3 = px.line(
        adoption_df,
        x="Quarter", y="ELN Adoption (%)",
        color="Team",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig3.add_vline(
        x=2, line_dash="dash", line_color="#C0392B",
        annotation_text="Digital Rollout"
    )
    fig3.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),
        margin=dict(t=20, b=10),
        yaxis=dict(range=[0, 105]),
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    st.markdown("#### 📊 Before vs After: Average Cycle Time")
    summary = (
        filtered_exp.groupby("Phase")["Avg Cycle Time (Days)"]
        .mean().reset_index()
    )
    summary["Phase"] = pd.Categorical(summary["Phase"], ["Pre-Digital", "Post-Digital"])
    summary = summary.sort_values("Phase")
    fig4 = px.bar(
        summary,
        x="Phase", y="Avg Cycle Time (Days)",
        color="Phase",
        color_discrete_map={"Pre-Digital": "#E74C3C", "Post-Digital": "#27AE60"},
        text_auto=".1f",
    )
    fig4.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False,
        margin=dict(t=20, b=10),
    )
    st.plotly_chart(fig4, use_container_width=True)

# ─────────────────────────────────────────────
# GENAI INSIGHTS SECTION
# ─────────────────────────────────────────────
st.divider()
st.markdown("### 🤖 Ask the Data — GenAI Insights")
st.markdown(
    "Ask a plain-English question about the R&D data. "
    "Powered by Claude (Anthropic)."
)

# Build a data summary to pass to Claude as context
def build_data_context():
    exp_summary = exp_df.groupby(["Quarter", "Phase"])["Avg Cycle Time (Days)"].mean().reset_index()
    cost_summary = cost_df.groupby(["Quarter", "Phase"])["Quarterly Savings ($)"].sum().reset_index()
    adoption_summary = adoption_df.groupby(["Quarter"])["ELN Adoption (%)"].mean().reset_index()

    return f"""
You are an analyst assistant for an R&D Digital Transformation dashboard at a CPG/Life Sciences company.
Answer questions using only the data below. Be concise, specific, and cite numbers where relevant.

EXPERIMENT CYCLE TIME (avg days per quarter):
{exp_summary.to_string(index=False)}

COST SAVINGS (quarterly total $):
{cost_summary.to_string(index=False)}

ELN ADOPTION (avg % across teams):
{adoption_summary.to_string(index=False)}

KEY CONTEXT:
- Digital transformation rollout began Q3 2023
- Pre-Digital = Q1-Q2 2023
- Post-Digital = Q3 2023 onward
- Product lines tracked: Haircare, Skincare, Body Wash, Oral Care
- Teams tracked: Formulation, Process Engineering, Quality, Regulatory
"""

# Example questions
st.markdown("**Try asking:**")
example_cols = st.columns(3)
examples = [
    "Which product line had the biggest cycle time improvement?",
    "What was the total cost savings after the digital rollout?",
    "How quickly did ELN adoption grow after Q3 2023?",
]
for i, ex in enumerate(examples):
    with example_cols[i]:
        if st.button(ex, use_container_width=True):
            st.session_state["user_question"] = ex

# Chat input
user_question = st.text_input(
    "Your question:",
    value=st.session_state.get("user_question", ""),
    placeholder="e.g. Which team had the slowest ELN adoption?",
    key="question_input"
)

if st.button("Get Insight", type="primary") and user_question:
    with st.spinner("Analyzing data..."):
        try:
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
            context = build_data_context()

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=400,
                messages=[
                    {
                        "role": "user",
                        "content": f"{context}\n\nQuestion: {user_question}"
                    }
                ]
            )
            answer = message.content[0].text
            st.markdown(f"<div class='insight-box'>{answer}</div>", unsafe_allow_html=True)

        except anthropic.AuthenticationError:
            st.error(
                "⚠️ API key not found. Set your ANTHROPIC_API_KEY environment variable to enable GenAI insights.\n\n"
                "Run: `export ANTHROPIC_API_KEY=your_key_here` then restart the app."
            )
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.divider()
st.markdown(
    "<small>Built by Maximos Stavrou · Portfolio Project · "
    "Data is synthetic and for demonstration purposes only · "
    "[LinkedIn](https://linkedin.com/in/maximos-stavrou)</small>",
    unsafe_allow_html=True
)
