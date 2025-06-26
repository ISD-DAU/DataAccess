import streamlit as st
import pandas as pd

# Load your CSV (update URL accordingly)
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

GITHUB_CSV_URL = "https://raw.githubusercontent.com/ISD-DAU/DataAccess/main/FB%20and%20instagram.csv"
df = load_data(GITHUB_CSV_URL)

def format_access(value):
    return "✅" if value == "Y" else "❌" if value == "N" else value

st.title("Social Media Data Access Explorer")

# Start with full data
filtered_df = df.copy()

# Platform filter
platform_options = sorted(filtered_df["Platform"].dropna().unique())
platform_filter = st.multiselect("Platform", platform_options)
if platform_filter:
    filtered_df = filtered_df[filtered_df["Platform"].isin(platform_filter)]

# Space filter
space_options = sorted(filtered_df["Space"].dropna().unique())
space_filter = st.multiselect("Space", space_options)
if space_filter:
    filtered_df = filtered_df[filtered_df["Space"].isin(space_filter)]

# Data Point filter
datapoint_options = sorted(filtered_df["Data Point"].dropna().unique())
datapoint_filter = st.multiselect("Data Point", datapoint_options)
if datapoint_filter:
    filtered_df = filtered_df[filtered_df["Data Point"].isin(datapoint_filter)]

# MCL UI filter
mcl_ui_options = sorted(filtered_df["MCL UI"].dropna().unique())
mcl_ui_filter = st.multiselect("MCL UI", mcl_ui_options)
if mcl_ui_filter:
    filtered_df = filtered_df[filtered_df["MCL UI"].isin(mcl_ui_filter)]

# MCL API filter
mcl_api_options = sorted(filtered_df["MCL API"].dropna().unique())
mcl_api_filter = st.multiselect("MCL API", mcl_api_options)
if mcl_api_filter:
    filtered_df = filtered_df[filtered_df["MCL API"].isin(mcl_api_filter)]

# Brandwatch filter
brandwatch_options = sorted(filtered_df["Brandwatch"].dropna().unique())
brandwatch_filter = st.multiselect("Brandwatch", brandwatch_options)
if brandwatch_filter:
    filtered_df = filtered_df[filtered_df["Brandwatch"].isin(brandwatch_filter)]

# Format Y/N columns
columns_to_format = ["MCL UI", "MCL API", "Brandwatch"]
for col in columns_to_format:
    if col in filtered_df.columns:
        filtered_df[col] = filtered_df[col].apply(format_access)

# Results
st.subheader(f"Filtered Results ({len(filtered_df)} rows)")

# Optional CSS tweaks
st.markdown("""
    <style>
    .stDataFrame td {
        white-space: normal !important;
        word-wrap: break-word !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.dataframe(filtered_df, use_container_width=True, height=700)

# Download button
csv = filtered_df.to_csv(index=False)
st.download_button("Download Filtered Data as CSV", csv, "filtered_data.csv", "text/csv")
