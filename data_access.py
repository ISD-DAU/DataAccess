import streamlit as st
import pandas as pd

# URL to your raw Excel file on GitHub
GITHUB_XLSX_URL = "https://raw.githubusercontent.com/ISD-DAU/DataAccess/main/FB%20and%20instagram.xlsx"

st.title("Social Media Data Access Explorer")

# Load Excel file from GitHub
@st.cache_data
def load_data(url):
    df = pd.read_excel(url)
    return df

df = load_data(GITHUB_XLSX_URL)

st.subheader("Filter Options")

# Create dropdown filters
platform_filter = st.selectbox("Platform", options=["All"] + sorted(df["Platform"].dropna().unique().tolist()))
space_filter = st.selectbox("Space", options=["All"] + sorted(df["Space"].dropna().unique().tolist()))
datapoint_filter = st.selectbox("Data Point", options=["All"] + sorted(df["Data Point"].dropna().unique().tolist()))
mcl_ui_filter = st.selectbox("MCL UI", options=["All"] + sorted(df["MCL UI"].dropna().unique().tolist()))
mcl_api_filter = st.selectbox("MCL API", options=["All"] + sorted(df["MCL API"].dropna().unique().tolist()))
brandwatch_filter = st.selectbox("Brandwatch", options=["All"] + sorted(df["Brandwatch"].dropna().unique().tolist()))

# Apply filters
filtered_df = df.copy()

if platform_filter != "All":
    filtered_df = filtered_df[filtered_df["Platform"] == platform_filter]

if space_filter != "All":
    filtered_df = filtered_df[filtered_df["Space"] == space_filter]

if datapoint_filter != "All":
    filtered_df = filtered_df[filtered_df["Data Point"] == datapoint_filter]

if mcl_ui_filter != "All":
    filtered_df = filtered_df[filtered_df["MCL UI"] == mcl_ui_filter]

if mcl_api_filter != "All":
    filtered_df = filtered_df[filtered_df["MCL API"] == mcl_api_filter]

if brandwatch_filter != "All":
    filtered_df = filtered_df[filtered_df["Brandwatch"] == brandwatch_filter]

# Display results
st.subheader(f"Filtered Results ({len(filtered_df)} rows)")
st.dataframe(filtered_df)

# Optional download button
csv = filtered_df.to_csv(index=False)
st.download_button("Download Filtered Data as CSV", csv, "filtered_data.csv", "text/csv")
