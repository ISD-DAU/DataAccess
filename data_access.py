import streamlit as st
import pandas as pd

# Load your CSV (update URL accordingly)
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

GITHUB_CSV_URL = "https://raw.githubusercontent.com/ISD-DAU/DataAccess/main/FB%20and%20instagram.csv"
df = load_data(GITHUB_CSV_URL)

def format_access(value):
    if value == "Y":
        return "✅"
    elif value == "N":
        return "❌"
    else:
        return value

st.title("Social Media Data Access Explorer")

# Step 1: Start with full data
filtered_df = df.copy()

# Step 2: Get current options based on filtered_df
platforms = sorted(filtered_df["Platform"].dropna().unique())
platform_filter = st.multiselect("Platform", options=platforms)

# Apply filter (OR logic)
if platform_filter:
    filtered_df = filtered_df[filtered_df["Platform"].isin(platform_filter)]

# Now get possible "Space" options *after* platform filtering
spaces = sorted(filtered_df["Space"].dropna().unique())
space_filter = st.multiselect("Space", options=spaces)

if space_filter:
    filtered_df = filtered_df[filtered_df["Space"].isin(space_filter)]

# Same for Data Point
datapoints = sorted(filtered_df["Data Point"].dropna().unique())
datapoint_filter = st.multiselect("Data Point", options=datapoints)

if datapoint_filter:
    filtered_df = filtered_df[filtered_df["Data Point"].isin(datapoint_filter)]

# MCL UI
mcl_uis = sorted(filtered_df["MCL UI"].dropna().unique())
mcl_ui_filter = st.multiselect("MCL UI", options=mcl_uis)

if mcl_ui_filter:
    filtered_df = filtered_df[filtered_df["MCL UI"].isin(mcl_ui_filter)]

# MCL API
mcl_apis = sorted(filtered_df["MCL API"].dropna().unique())
mcl_api_filter = st.multiselect("MCL API", options=mcl_apis)

if mcl_api_filter:
    filtered_df = filtered_df[filtered_df["MCL API"].isin(mcl_api_filter)]

# Brandwatch
brandwatches = sorted(filtered_df["Brandwatch"].dropna().unique())
brandwatch_filter = st.multiselect("Brandwatch", options=brandwatches)

if brandwatch_filter:
    filtered_df = filtered_df[filtered_df["Brandwatch"].isin(brandwatch_filter)]

# Replace Y/N with icons in specific columns
columns_to_format = ["MCL UI", "MCL API", "Brandwatch"]

for col in columns_to_format:
    if col in filtered_df.columns:
        filtered_df[col] = filtered_df[col].apply(format_access)

# Final results
st.subheader(f"Filtered Results ({len(filtered_df)} rows)")
st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False)
st.download_button("Download Filtered Data as CSV", csv, "filtered_data.csv", "text/csv")
