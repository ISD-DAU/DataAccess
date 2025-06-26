import streamlit as st
import pandas as pd

# URL to your raw Excel file on GitHub
GITHUB_CSV_URL = "https://raw.githubusercontent.com/ISD-DAU/DataAccess/refs/heads/main/FB%20and%20instagram.csv"

st.title("Social Media Data Access Explorer")

# Load Excel file from GitHub
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data(GITHUB_CSV_URL)

st.subheader("Filter Options")

# Multiselect filters
platform_filter = st.multiselect("Platform", options=sorted(df["Platform"].dropna().unique()), default=[])
space_filter = st.multiselect("Space", options=sorted(df["Space"].dropna().unique()), default=[])
datapoint_filter = st.multiselect("Data Point", options=sorted(df["Data Point"].dropna().unique()), default=[])
mcl_ui_filter = st.multiselect("MCL UI", options=sorted(df["MCL UI"].dropna().unique()), default=[])
mcl_api_filter = st.multiselect("MCL API", options=sorted(df["MCL API"].dropna().unique()), default=[])
brandwatch_filter = st.multiselect("Brandwatch", options=sorted(df["Brandwatch"].dropna().unique()), default=[])

# Apply filters
filtered_df = df.copy()

if platform_filter:
    filtered_df = filtered_df[filtered_df["Platform"].isin(platform_filter)]

if space_filter:
    filtered_df = filtered_df[filtered_df["Space"].isin(space_filter)]

if datapoint_filter:
    filtered_df = filtered_df[filtered_df["Data Point"].isin(datapoint_filter)]

if mcl_ui_filter:
    filtered_df = filtered_df[filtered_df["MCL UI"].isin(mcl_ui_filter)]

if mcl_api_filter:
    filtered_df = filtered_df[filtered_df["MCL API"].isin(mcl_api_filter)]

if brandwatch_filter:
    filtered_df = filtered_df[filtered_df["Brandwatch"].isin(brandwatch_filter)]

# Display results
st.subheader(f"Filtered Results ({len(filtered_df)} rows)")
st.dataframe(filtered_df)

# Optional download button
csv = filtered_df.to_csv(index=False)
st.download_button("Download Filtered Data as CSV", csv, "filtered_data.csv", "text/csv")
