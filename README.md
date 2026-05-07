# R\&D Digital Transformation ROI Dashboard

A portfolio project by **Maximos Stavrou** demonstrating how CPG and Life Sciences companies can measure, track, and communicate the ROI of digital transformation initiatives in R\&D.

Built with Python, Streamlit, Plotly, and Claude (Anthropic) for GenAI-powered data insights.

\---

## What This Project Demonstrates

* **Data analysis \& visualization** — KPI tracking, before/after comparisons, trend analysis across product lines and teams
* **GenAI integration** — Natural language querying of operational data using Claude API
* **Domain expertise** — Realistic simulation of R\&D metrics (experiment cycle time, ELN adoption, cost savings) from CPG/Life Sciences context
* **Program thinking** — Dashboard is framed around a digital transformation program with clear phases, milestones, and outcomes

\---

## Features

* **KPI Summary Cards** — High-level metrics: cycle time reduction, total savings, ELN adoption rate
* **Interactive Charts** — Experiment cycle time trends, cumulative cost savings, ELN adoption by team, pre/post comparison
* **Filters** — Slice data by product line and quarter
* **GenAI Insights** — Ask plain-English questions about the data; powered by Claude

\---

## Tech Stack

|Tool|Purpose|
|-|-|
|Python|Core language|
|Streamlit|Dashboard framework|
|Plotly|Interactive charts|
|Pandas|Data manipulation|
|Anthropic (Claude)|GenAI insights engine|

\---

## Getting Started

### 1\. Clone the repo

```bash
git clone https://github.com/YOUR\_USERNAME/rd-transformation-dashboard
cd rd-transformation-dashboard
```

### 2\. Install dependencies

```bash
pip install -r requirements.txt
```

### 3\. Set your Anthropic API key

```bash
export ANTHROPIC\_API\_KEY=your\_api\_key\_here
```

Get a free API key at [console.anthropic.com](https://console.anthropic.com)

### 4\. Run the dashboard

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`

\---

## Project Structure

```
rd-transformation-dashboard/
├── app.py           # Main dashboard — all UI, charts, and GenAI logic
├── data.py          # Synthetic data generator — simulates R\&D operational metrics
├── requirements.txt # Python dependencies
└── README.md        # This file
```

\---

## The Business Context

This dashboard simulates the impact of a digital transformation program in an R\&D organization — specifically the rollout of an Electronic Lab Notebook (ELN) and digital workflow platform (e.g., BIOVIA, LabVantage) beginning in Q3 2023.

Key metrics tracked:

* **Experiment cycle time** — Days from experiment start to signed-off results
* **Cost savings** — Quarterly and cumulative savings from process improvements
* **ELN adoption** — % of lab work captured digitally vs. paper-based

The GenAI component lets stakeholders query the data in plain English — removing the need to know SQL or navigate complex BI tools.

\---

## How to Extend This Project

Ideas to make it more impressive:

* Connect to a real data source (CSV upload, Google Sheets, or a mock API)
* Add user authentication for a multi-team view
* Build a "program health" score that aggregates KPIs into a single RAG status
* Export a PDF summary report from the dashboard
* Add forecasting — predict cost savings for next 4 quarters based on trend

\---

## About

Built as a portfolio piece to demonstrate technical program management, data analysis, and GenAI integration skills in the context of R\&D digital transformation.

**Maximos Stavrou** | [LinkedIn](https://linkedin.com/in/maximos-stavrou) | maximos.stavrou@gmail.com

