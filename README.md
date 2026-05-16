his project creates a modern dashboard for:

Latest LLM models
Token limits
Pricing
Context windows
Input/output cost
Use cases
Provider comparison
Search and filtering

Recommended stack:

Python
Streamlit
Pandas
Plotly
Project Structure
llm-dashboard/
│
├── app.py
├── requirements.txt
├── models.json
└── README.md
requirements.txt
streamlit
pandas
plotly
requests
models.json
[
  {
    "provider": "OpenAI",
    "model": "GPT-5",
    "context_window": "256K",
    "input_price": 0.005,
    "output_price": 0.015,
    "best_for": "Reasoning, coding, agents",
    "speed": "Fast"
  },
  {
    "provider": "Anthropic",
    "model": "Claude 3.7 Sonnet",
    "context_window": "200K",
    "input_price": 0.003,
    "output_price": 0.015,
    "best_for": "Long context, analysis",
    "speed": "Medium"
  },
  {
    "provider": "Google",
    "model": "Gemini 2.5 Pro",
    "context_window": "1M",
    "input_price": 0.0025,
    "output_price": 0.01,
    "best_for": "Massive context, multimodal",
    "speed": "Fast"
  },
  {
    "provider": "Meta",
    "model": "Llama 4",
    "context_window": "128K",
    "input_price": 0.001,
    "output_price": 0.003,
    "best_for": "Open-source deployment",
    "speed": "Fast"
  }
]
app.py
import json
import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="LLM Dashboard",
    layout="wide"
)


st.title("🚀 LLM Models Dashboard")
st.markdown("Compare latest AI/LLM models, pricing and token limits")


# Load data
with open("models.json", "r") as f:
    data = json.load(f)


# DataFrame


df = pd.DataFrame(data)


# Sidebar Filters
st.sidebar.header("Filters")


provider_filter = st.sidebar.multiselect(
    "Select Provider",
    options=df["provider"].unique(),
    default=df["provider"].unique()
)


speed_filter = st.sidebar.multiselect(
    "Select Speed",
    options=df["speed"].unique(),
    default=df["speed"].unique()
)


filtered_df = df[
    (df["provider"].isin(provider_filter)) &
    (df["speed"].isin(speed_filter))
]


# Metrics
col1, col2, col3 = st.columns(3)


with col1:
    st.metric("Total Models", len(filtered_df))


with col2:
    cheapest = filtered_df["input_price"].min()
    st.metric("Lowest Input Price", f"${cheapest}/1K")


with col3:
    max_context = filtered_df["context_window"].max()
    st.metric("Largest Context", max_context)


st.divider()


# Table
st.subheader("📊 Model Comparison")
st.dataframe(filtered_df, use_container_width=True)


Run the Dashboard
pip install -r requirements.txt

Run:

streamlit run app.py
Advanced Features To Add
Live APIs

Fetch live pricing/model data from:

OpenAI
Anthropic
Google Gemini
AWS Bedrock
Together AI
Groq
Ollama
HuggingFace
Enterprise Features

You can later add:

Authentication
Multi-user dashboards
Token usage analytics
AI cost estimation
GPU monitoring
Model latency tracking
RAG performance metrics
AI observability
Prompt analytics
LLM benchmarking
Recommended Next Upgrade
Add Live Model APIs

Example:

import requests


response = requests.get("https://api.openai.com/v1/models")
Recommended Architecture
Frontend Dashboard (Streamlit)
        ↓
FastAPI Backend
        ↓
LLM Provider APIs
        ↓
Caching Layer (Redis)
        ↓
Database (Postgres)
Best Deployment Options
Platform	Recommended
AWS ECS	Production
Kubernetes	Enterprise
EC2	Small Scale
Streamlit Cloud	Demo
Docker	Local Dev
Future AI Ops Features

You can evolve this into:

LLMOps platform
AI governance dashboard
Cost optimization engine
Agent observability system
AI marketplace
Enterprise AI portal

This project aligns very well with your AI + DevOps + LLMOps learning path.

I created a complete Python-based LLM dashboard project with:

Streamlit UI
Model comparison table
Token/context window tracking
Pricing analytics
Provider filters
Use-case sections
Plotly charts
Sample JSON model dataset
Enterprise architecture guidance
Deployment instructions

It’s designed so you can later extend it into:

AI observability platform
LLMOps dashboard
RAG analytics portal
Token cost optimizer
Multi-provider AI gateway
