import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from groq import Groq
from fredapi import Fred
from dotenv import load_dotenv

load_dotenv()

# ── CLIENTS ──────────────────────────────────────────────────────────────────
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
fred = Fred(api_key=os.getenv("FRED_API_KEY"))

# ── FRED SERIES ───────────────────────────────────────────────────────────────
SERIES = {
    "Economic Policy Uncertainty (EPU)": "USEPUINDXD",
    "Federal Funds Rate": "FEDFUNDS",
    "CPI Inflation": "CPIAUCSL",
    "Unemployment Rate": "UNRATE",
    "10Y Treasury Yield": "DGS10",
}

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="MacroPolicy AI Analyst",  layout="wide")
st.title(" MacroPolicy AI Analyst")
st.markdown("*An agentic macro intelligence tool powered by FRED data and Groq LLM*")

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.header("Settings")
selected_series = st.sidebar.selectbox("Select Macro Indicator", list(SERIES.keys()))
years = st.sidebar.slider("Years of history", 2, 20, 10)

# ── FETCH FRED DATA ───────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_data(series_id, years):
    data = fred.get_series(series_id)
    data = data.dropna()
    cutoff = pd.Timestamp.today() - pd.DateOffset(years=years)
    return data[data.index >= cutoff]

try:
    series_data = fetch_data(SERIES[selected_series], years)

    # ── CHART ─────────────────────────────────────────────────────────────────
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=series_data.index,
        y=series_data.values,
        mode="lines",
        line=dict(color="#2563eb", width=2),
        name=selected_series
    ))
    fig.update_layout(
        title=f"{selected_series} — Last {years} Years",
        xaxis_title="Date",
        yaxis_title="Value",
        template="plotly_white",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── SUMMARY STATS ─────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latest Value", f"{series_data.iloc[-1]:.2f}")
    col2.metric("1Y Avg", f"{series_data[series_data.index >= series_data.index[-1] - pd.DateOffset(years=1)].mean():.2f}")
    col3.metric("Max (period)", f"{series_data.max():.2f}")
    col4.metric("Min (period)", f"{series_data.min():.2f}")

    # ── AI ANALYST ────────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Ask the AI Analyst")
    st.markdown("Ask anything about this indicator, macro trends, or policy implications.")

    user_question = st.text_area(
        "Your question:",
        placeholder="e.g. What does the current EPU trend suggest about investor sentiment?"
    )

    if st.button("Analyse", type="primary"):
        if user_question.strip() == "":
            st.warning("Please type a question first.")
        else:
            # Build context from real data
            recent = series_data[series_data.index >= series_data.index[-1] - pd.DateOffset(years=1)]
            data_context = f"""
You are a macro policy analyst with expertise in economic uncertainty, monetary policy, and forecasting.

Current indicator: {selected_series}
Latest value: {series_data.iloc[-1]:.2f}
12-month average: {recent.mean():.2f}
12-month high: {recent.max():.2f}
12-month low: {recent.min():.2f}
Period covered: {series_data.index[0].strftime('%b %Y')} to {series_data.index[-1].strftime('%b %Y')}

The user is asking: {user_question}

Respond as a senior analyst would in a structured brief:
1. Current reading and what it signals
2. Recent trend interpretation
3. Policy or investment implication
4. Key risks to watch

Be concise, data-grounded, and avoid generic statements.
"""
            with st.spinner("Analysing..."):
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": data_context}],
                    temperature=0.4,
                    max_tokens=600
                )
                answer = response.choices[0].message.content

            st.markdown("### Analyst Brief")
            st.markdown(answer)

except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.info("Check your FRED API key in the .env file.")