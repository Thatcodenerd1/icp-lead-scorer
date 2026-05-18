"""Streamlit ICP Scorer UI — interactive lead scoring dashboard."""
import streamlit as st, pandas as pd, plotly.express as px
from scorer import score_company
st.set_page_config(page_title="ICP Lead Scorer",layout="wide")
st.title("ICP Lead Scorer")
with st.sidebar:
    st.header("ICP Config")
    h_min=st.number_input("Min headcount",value=50); h_max=st.number_input("Max headcount",value=500)
    industries=st.multiselect("Target industries",["SaaS","FinTech","HealthTech","EdTech","DevTools","Security","Data & AI"],default=["SaaS","FinTech","HealthTech"])
    stages=st.multiselect("Funding stages",["Seed","Series A","Series B","Series C","Growth"],default=["Series A","Series B","Series C"])
    min_g=st.slider("Min growth %",0,50,10)
icp={"ideal_headcount_range":[h_min,h_max],"target_industries":industries,"target_tech_stack":["Salesforce","HubSpot","Segment","Stripe","Snowflake"],"funding_stages":stages,"min_headcount_growth_pct":min_g,"weights":{"headcount":0.25,"industry":0.20,"tech_stack":0.20,"funding":0.20,"growth":0.15}}
f=st.file_uploader("Upload companies CSV",type=["csv"])
if f:
    df=pd.read_csv(f)
    scored=df.apply(lambda r:pd.Series(score_company(r.to_dict(),icp)),axis=1).sort_values('icp_score',ascending=False)
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Total",len(scored)); c2.metric("T1 (80+)",len(scored[scored.tier=='T1']))
    c3.metric("T2 (60-79)",len(scored[scored.tier=='T2'])); c4.metric("Avg Score",f"{scored.icp_score.mean():.0f}")
    st.plotly_chart(px.histogram(scored,x='icp_score',color='tier',title='Score Distribution',color_discrete_map={'T1':'#22c55e','T2':'#eab308','T3':'#f97316','No Fit':'#ef4444'}),use_container_width=True)
    cols=[c for c in ['company','industry','headcount','funding_stage','icp_score','tier'] if c in scored.columns]
    st.dataframe(scored[cols],use_container_width=True)
    st.download_button("Download CSV",scored.to_csv(index=False).encode(),"scored_leads.csv","text/csv")
else: st.info("Upload a CSV with: company, industry, headcount, funding_stage, headcount_growth_pct, tech_stack")
