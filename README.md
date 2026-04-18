# MacroPolicy AI Analyst

An agentic macro intelligence tool that combines live FRED economic data with LLM-powered analyst reasoning.

## What it does
- Pulls real-time macroeconomic indicators from FRED (EPU, CPI, Fed Funds Rate, Unemployment, 10Y Treasury)
- Visualises trends across a user-selected time window
- Accepts natural language questions and returns structured analyst briefs grounded in live data

## Tech Stack
- **Data:** FRED API (Federal Reserve Economic Data)
- **LLM:** Groq API (Llama 3.3 70B)
- **Frontend:** Streamlit
- **Libraries:** Pandas, Plotly, Python-dotenv

## How to run locally
```bash
git clone https://github.com/aarushiksharmads/macropolicy-ai-analyst
cd macropolicy-ai-analyst
pip install -r requirements.txt
streamlit run app.py
```

Add a `.env` file with:
GROQ_API_KEY=your_groq_key
FRED_API_KEY=your_fred_key
## Background
Built as an extension of my MSc thesis on forecasting Economic Policy Uncertainty (EPU) using ML-econometric ensembles. This tool makes that analysis accessible in real time via an agentic LLM interface.

## Live Demo
[Click here to open the app](https://macropolicy-ai-analyst-5edchlqkjzecthbmweoetk.streamlit.app/)