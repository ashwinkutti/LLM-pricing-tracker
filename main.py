import os
import json
import requests
import pandas as pd
import streamlit as st
import plotly.express as px

from bs4 import BeautifulSoup
from openai import OpenAI

# ------------------------------------------------
# OPENAI CLIENT
# ------------------------------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="LLM Pricing Dashboard",
    layout="wide"
)

# ------------------------------------------------
# TITLE
# ------------------------------------------------

st.title("🚀 LLM Pricing Dashboard")
st.markdown("Compare LLM pricing, context windows, parameters, and providers")

# ------------------------------------------------
# LOAD JSON
# ------------------------------------------------

try:

    with open("dynamic_models.json", "r") as f:
        data = json.load(f)

    st.success("✅ JSON Loaded Successfully")

except Exception as e:

    st.error(f"Failed to load JSON: {e}")
    st.stop()

# ------------------------------------------------
# SHOW RAW JSON
# ------------------------------------------------

with st.expander("🗂 Raw JSON Preview"):

    st.json(data[:5] if len(data) > 5 else data)

# ------------------------------------------------
# CREATE DATAFRAME
# ------------------------------------------------

try:

    df = pd.DataFrame(data)

    st.success("✅ DataFrame Created")

except Exception as e:

    st.error(f"DataFrame Error: {e}")
    st.stop()

# ------------------------------------------------
# CHECK EMPTY
# ------------------------------------------------

if df.empty:
    st.warning("⚠ No data available")
    st.stop()

# ------------------------------------------------
# REQUIRED COLUMNS
# ------------------------------------------------

required_columns = [
    "provider",
    "model",
    "input_price",
    "output_price"
]

for col in required_columns:

    if col not in df.columns:

        st.error(f"Missing column: {col}")
        st.stop()

# ------------------------------------------------
# CLEAN DATA
# ------------------------------------------------

df["input_price"] = pd.to_numeric(
    df["input_price"],
    errors="coerce"
).fillna(0)

df["output_price"] = pd.to_numeric(
    df["output_price"],
    errors="coerce"
).fillna(0)

# Fill missing optional fields

optional_columns = [
    "parameters",
    "context_window",
    "best_for",
    "speed"
]

for col in optional_columns:

    if col not in df.columns:
        df[col] = "Unknown"

    df[col] = df[col].fillna("Unknown")

# ------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------

st.sidebar.header("🔍 Filters")

providers = df["provider"].unique()

provider_filter = st.sidebar.multiselect(
    "Provider",
    providers,
    default=providers
)

speeds = df["speed"].unique()

speed_filter = st.sidebar.multiselect(
    "Speed",
    speeds,
    default=speeds
)

filtered_df = df[
    (df["provider"].isin(provider_filter)) &
    (df["speed"].isin(speed_filter))
]

# ------------------------------------------------
# METRICS
# ------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Models",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Lowest Input Price",
        f"${filtered_df['input_price'].min():,.4f}"
    )

with col3:
    st.metric(
        "Highest Output Price",
        f"${filtered_df['output_price'].max():,.4f}"
    )

with col4:
    st.metric(
        "Providers",
        filtered_df["provider"].nunique()
    )

# ------------------------------------------------
# FORMAT DISPLAY TABLE
# ------------------------------------------------

display_df = filtered_df.copy()

display_df["input_price"] = display_df["input_price"].apply(
    lambda x: f"${x:,.4f}"
)

display_df["output_price"] = display_df["output_price"].apply(
    lambda x: f"${x:,.4f}"
)

# ------------------------------------------------
# TABLE
# ------------------------------------------------

st.divider()

st.subheader("📊 Model Comparison")

display_columns = [
    "provider",
    "model",
    "parameters",
    "context_window",
    "input_price",
    "output_price",
    "best_for",
    "speed"
]

available_columns = [
    col for col in display_columns
    if col in display_df.columns
]

st.dataframe(
    display_df[available_columns],
    use_container_width=True
)

# ------------------------------------------------
# INPUT PRICE CHART
# ------------------------------------------------

st.divider()

st.subheader("💰 Input Pricing Comparison")

try:

    fig_input = px.bar(
        filtered_df,
        x="model",
        y="input_price",
        color="provider",
        title="Input Token Pricing",
        hover_data=[
            "parameters",
            "context_window",
            "best_for"
        ]
    )

    st.plotly_chart(
        fig_input,
        use_container_width=True
    )

except Exception as e:

    st.error(f"Input Chart Error: {e}")

# ------------------------------------------------
# OUTPUT PRICE CHART
# ------------------------------------------------

st.subheader("📈 Output Pricing Comparison")

try:

    fig_output = px.bar(
        filtered_df,
        x="model",
        y="output_price",
        color="provider",
        title="Output Token Pricing",
        hover_data=[
            "parameters",
            "context_window",
            "best_for"
        ]
    )

    st.plotly_chart(
        fig_output,
        use_container_width=True
    )

except Exception as e:

    st.error(f"Output Chart Error: {e}")

# ------------------------------------------------
# MODEL DETAILS
# ------------------------------------------------

st.divider()

st.subheader("🧠 Model Details")

for _, row in filtered_df.iterrows():

    with st.expander(f"{row['model']} ({row['provider']})"):

        st.write(f"### {row['model']}")

        st.write(f"**Provider:** {row['provider']}")
        st.write(f"**Parameters:** {row['parameters']}")
        st.write(f"**Context Window:** {row['context_window']}")
        st.write(f"**Input Price:** ${row['input_price']:,.4f}")
        st.write(f"**Output Price:** ${row['output_price']:,.4f}")
        st.write(f"**Speed:** {row['speed']}")
        st.write(f"**Best For:** {row['best_for']}")

# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.divider()

st.success("✅ Dashboard Loaded Successfully")