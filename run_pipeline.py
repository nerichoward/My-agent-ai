
import streamlit as st
import pandas as pd
import json
import plotly.express as px
from pathlib import Path

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Agentic Options Suite", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
DATA_PATH = Path("../shared/AAPL_raw.json")

def load_data():
    if not DATA_PATH.exists():
        st.error("No data found! Waiting for Quant Agent...")
        return None
    with open(DATA_PATH, "r") as f:
        return json.load(f)

data = load_data()

if data:
    # --- HEADER ---
    st.title(f"📊 {data['ticker']} Options Analysis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Underlying Price", f"${data['price']:.2f}")
    with col2:
        st.metric("Implied Volatility", f"{data['iv']:.1f}%")
    with col3:
        # Highlighting the Strategy Agent's specific output
        st.success(f"Strategy: {data.get('recommendation', 'Analyzing...')}")

    # --- VISUALIZATION ---
    st.divider()
    st.subheader("Volatility & Strike Analysis")
    
    # Simulate a chart based on the data provided
    df = pd.DataFrame({
        "Strike": data['strikes'],
        "Delta": [0.8, 0.6, 0.4, 0.2] # Agent infers visualization needs
    })
    
    fig = px.bar(df, x="Strike", y="Delta", 
                 title="Option Delta per Strike",
                 template="plotly_dark", 
                 color_continuous_scale="Viridis")
    st.plotly_chart(fig, use_container_width=True)

    # --- RAW DATA VIEW ---
    with st.expander("View Raw Agent Handoff (JSON)"):
        st.json(data)
else:
    st.info("The pipeline is currently running. Please refresh in a moment.")
