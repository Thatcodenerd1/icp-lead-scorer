"""
ICP Lead Scoring Engine
Scores companies against a configurable Ideal Customer Profile (ICP).
"""

import json
import csv
import argparse
import pandas as pd

def load_icp(config_path):
    with open(config_path) as f:
        return json.load(f)

def score_headcount(headcount, ideal_range):
    lo, hi = ideal_range
    if lo <= headcount <= hi:
        return 10
    elif headcount < lo:
        return max(0, 10 - int((lo - headcount) / lo * 10))
    else:
        return max(0, 10 - int((headcount - hi) / hi * 5))

def score_industry(industry, target_industries):
    return 10 if industry in target_industries else 2

def score_tech_stack(tech_stack, target_stack):
    if not tech_stack:
        return 5
    techs = [t.strip() for t in tech_stack.split(',')]
    matches = sum(1 for t in techs if t in target_stack)
    return min(10, matches * 3 + 1)

def score_funding(stage, target_stages):
    return 10 if stage in target_stages else 3

def score_growth(growth_pct, min_growth):
    if growth_pct >= min_growth * 2:
        return 10
    elif growth_pct >= min_growth:
        return 7
    elif growth_pct > 0:
        return 4
    return 1

def score_company(row, icp):
    w = icp.get('weights', {})
    scores = {
        'headcount': score_headcount(int(row.get('headcount', 0)), icp['ideal_headcount_range']),
        'industry': score_industry(row.get('industry', ''), icp['target_industries']),
        'tech_stack': score_tech_stack(row.get('tech_stack', ''), icp['target_tech_stack']),
        'funding': score_funding(row.get('funding_stage', ''), icp['funding_stages']),
        'growth': score_growth(float(row.get('headcount_growth_pct', 0)), icp.get('min_headcount_growth_pct', 10))
    }
    total = sum(scores[k] * w.get(k, 0.2) for k in scores)
    icp_score = round(total * 10)
    tier = 'T1' if icp_score >= 80 else 'T2' if icp_score >= 60 else 'T3' if icp_score >= 40 else 'No Fit'
    return {**row, **{f'score_{k}': v for k, v in scores.items()}, 'icp_score': icp_score, 'tier': tier}

def run_scorer(input_path, icp_path, output_path=None, output_format='csv'):
    icp = load_icp(icp_path)
    df = pd.read_csv(input_path)
    scored = df.apply(lambda row: pd.Series(score_company(row.to_dict(), icp)), axis=1)
    scored = scored.sort_values('icp_score', ascending=False).reset_index(drop=True)
    if output_path:
        if output_format == 'excel':
            scored.to_excel(output_path, index=False)
        else:
            scored.to_csv(output_path, index=False)
        print(f"Saved scored leads to {output_path}")
    else:
        print(scored[['company', 'industry', 'headcount', 'funding_stage', 'icp_score', 'tier']].to_string())
    return scored

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--icp', required=True)
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--format', default='csv', choices=['csv', 'excel'])
    args = parser.parse_args()
    run_scorer(args.input, args.icp, args.output, args.format)
