"""
data.py — Generates synthetic R&D operational data for the dashboard.

In a real company, this data would come from an ELN, LIMS, or PLM system.
Here we simulate realistic CPG/Life Sciences R&D metrics.
"""

import pandas as pd
import numpy as np

# Set a random seed so data is consistent every time
np.random.seed(42)

PRODUCT_LINES = ["Haircare", "Skincare", "Body Wash", "Oral Care"]
TEAMS = ["Formulation", "Process Engineering", "Quality", "Regulatory"]
QUARTERS = ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"]

# --- Digital Transformation "Before vs After" cutoff ---
# Simulates the impact of implementing an ELN/digital workflow (e.g., BIOVIA)
DIGITAL_CUTOFF = "Q3 2023"  # Everything from Q3 2023 onward = post-transformation


def get_experiment_data():
    """
    Simulates experiment cycle time data across product lines and quarters.
    Cycle time = days from experiment start to results sign-off.
    Digital transformation reduces cycle time meaningfully.
    """
    rows = []
    for quarter in QUARTERS:
        is_post_digital = QUARTERS.index(quarter) >= QUARTERS.index(DIGITAL_CUTOFF)
        for product in PRODUCT_LINES:
            # Post-digital: faster cycle times, less variance
            base_days = 18 if is_post_digital else 32
            variance = 3 if is_post_digital else 8
            n_experiments = np.random.randint(12, 25)
            cycle_times = np.random.normal(base_days, variance, n_experiments)
            cycle_times = np.clip(cycle_times, 5, 60)  # realistic bounds

            rows.append({
                "Quarter": quarter,
                "Product Line": product,
                "Avg Cycle Time (Days)": round(cycle_times.mean(), 1),
                "Num Experiments": n_experiments,
                "Phase": "Post-Digital" if is_post_digital else "Pre-Digital"
            })
    return pd.DataFrame(rows)


def get_cost_savings_data():
    """
    Simulates cumulative cost savings by product line over time.
    Savings accelerate post-digital transformation.
    """
    rows = []
    cumulative = {p: 0 for p in PRODUCT_LINES}
    for quarter in QUARTERS:
        is_post_digital = QUARTERS.index(quarter) >= QUARTERS.index(DIGITAL_CUTOFF)
        for product in PRODUCT_LINES:
            # Post-digital: higher quarterly savings
            quarterly_saving = np.random.uniform(80000, 200000) if is_post_digital else np.random.uniform(20000, 60000)
            cumulative[product] += quarterly_saving
            rows.append({
                "Quarter": quarter,
                "Product Line": product,
                "Quarterly Savings ($)": round(quarterly_saving, 0),
                "Cumulative Savings ($)": round(cumulative[product], 0),
                "Phase": "Post-Digital" if is_post_digital else "Pre-Digital"
            })
    return pd.DataFrame(rows)


def get_eln_adoption_data():
    """
    Simulates ELN (Electronic Lab Notebook) adoption rates by team over time.
    Adoption grows after the digital transformation rollout.
    """
    rows = []
    for quarter in QUARTERS:
        q_idx = QUARTERS.index(quarter)
        for team in TEAMS:
            if q_idx < QUARTERS.index(DIGITAL_CUTOFF):
                adoption = np.random.uniform(5, 20)  # low pre-digital
            else:
                # Ramp up over time post-rollout
                ramp = min((q_idx - QUARTERS.index(DIGITAL_CUTOFF) + 1) * 15, 85)
                adoption = np.random.uniform(ramp, min(ramp + 15, 98))
            rows.append({
                "Quarter": quarter,
                "Team": team,
                "ELN Adoption (%)": round(adoption, 1),
                "Phase": "Post-Digital" if q_idx >= QUARTERS.index(DIGITAL_CUTOFF) else "Pre-Digital"
            })
    return pd.DataFrame(rows)


def get_kpi_summary():
    """
    Returns high-level KPI summary cards for the dashboard header.
    """
    exp_data = get_experiment_data()
    cost_data = get_cost_savings_data()
    adoption_data = get_eln_adoption_data()

    pre = exp_data[exp_data["Phase"] == "Pre-Digital"]["Avg Cycle Time (Days)"].mean()
    post = exp_data[exp_data["Phase"] == "Post-Digital"]["Avg Cycle Time (Days)"].mean()
    cycle_improvement = round(((pre - post) / pre) * 100, 1)

    total_savings = cost_data[cost_data["Phase"] == "Post-Digital"]["Quarterly Savings ($)"].sum()

    latest_adoption = adoption_data[adoption_data["Quarter"] == "Q4 2024"]["ELN Adoption (%)"].mean()

    return {
        "cycle_time_reduction": f"{cycle_improvement}%",
        "total_savings": f"${total_savings / 1_000_000:.1f}M",
        "eln_adoption": f"{round(latest_adoption, 1)}%",
        "experiments_run": str(exp_data["Num Experiments"].sum()),
    }
