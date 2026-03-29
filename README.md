# ICP Lead Scoring Model

An interactive lead scoring tool that takes a list of companies and scores them against a configurable Ideal Customer Profile (ICP). Designed for early-stage GTM teams moving from founder-led, intuition-based outreach to a structured, data-driven process.

## The Problem

Most early-stage GTM teams prioritize outreach by gut feel — "this company looks like a good fit." This tool makes ICP-fit quantitative and auditable, so the whole team is targeting the same type of account.

## How Scoring Works

Each company is scored across 5 weighted dimensions:

| Dimension | Weight | Data Source |
|-----------|--------|-------------|
| Company size (headcount) | 25% | LinkedIn / Apollo |
| Industry fit | 20% | Manual tag or SIC code |
| Tech stack alignment | 20% | BuiltWith / Clearbit |
| Funding stage & recency | 20% | Crunchbase |
| Headcount growth (6-month) | 15% | LinkedIn |

Each dimension is scored 0-10. Final ICP score = weighted average x 10 = 0-100.

**Score bands:**
- 80-100: Tier 1 — Priority outreach, personalized sequence
- 60-79: Tier 2 — Include in campaign, lighter personalization
- 40-59: Tier 3 — Nurture list, lower-touch outreach
- 0-39: Not a fit — remove from active pipeline

## Setup

```bash
pip install pandas openpyxl streamlit plotly
```

## Usage

### CLI Mode
```bash
# Score a list of companies from CSV
python scorer.py --input companies.csv --icp icp_config.json --output scored_leads.csv
```

### Interactive Mode (Streamlit)
```bash
streamlit run app.py
# Opens browser UI: upload your account list, configure ICP weights, view scores interactively
```

### Excel Mode
```bash
# Generate a Salesforce-ready Excel file with scores + tier tags
python scorer.py --input companies.csv --icp icp_config.json --format excel --output salesforce_upload.xlsx
```

## ICP Configuration

Edit `icp_config.json` to define your ideal customer:

```json
{
  "ideal_headcount_range": [50, 500],
  "target_industries": ["SaaS", "FinTech", "HealthTech", "EdTech"],
  "target_tech_stack": ["Salesforce", "HubSpot", "Segment", "Stripe"],
  "funding_stages": ["Series A", "Series B", "Series C"],
  "min_headcount_growth_pct": 10,
  "weights": {
    "headcount": 0.25,
    "industry": 0.20,
    "tech_stack": 0.20,
    "funding": 0.20,
    "growth": 0.15
  }
}
```

## Sample Output

```
Company           Industry    Size   Funding    ICP Score   Tier
Acme SaaS Co      SaaS        230    Series B   87          T1 Priority
BetaFinance       FinTech     85     Series A   82          T1 Priority
GammaTech         HealthTech  410    Series C   74          T2 Include
DeltaHR           HRTech      1200   Growth     51          T3 Nurture
Epsilon Inc.      Retail      45     Seed       31          No Fit
```

## Files

```
icp-lead-scorer/
├── scorer.py             # Core scoring engine
├── app.py                # Streamlit interactive UI
├── icp_config.json       # ICP definition (edit this)
├── sample_companies.csv  # 20-row sample input
├── utils/
│   ├── normalizer.py     # Dimension scoring functions
│   └── exporter.py       # Excel/CSV export with Salesforce formatting
└── requirements.txt
```

## Background

Built to systematize the account prioritization work I did at Social Capital Inc. and 180 Degrees Consulting — where I was manually assessing "fit" for 30+ accounts at a time across multiple criteria. This tool makes that process repeatable, scalable, and explainable to the rest of the team.

---

*Part of [Mansi More's GTM & Growth Portfolio](https://github.com/Thatcodenerd1/gtm-growth-projects)*
