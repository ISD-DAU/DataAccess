import streamlit as st
import pandas as pd

# CSV URLs
METADATA_URL = "https://raw.githubusercontent.com/ISD-DAU/DataAccess/main/FB%20and%20instagram.csv"
TOPLINE_URL = "https://raw.githubusercontent.com/ISD-DAU/DataAccess/main/topline.csv"

# Cache loading
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

def format_access(value):
    return "✅" if value == "Y" else "❌" if value == "N" else value

# Sidebar navigation
page = st.sidebar.selectbox("Choose View", ["Detailed Metadata", "Topline"])

st.title("Social Media Data Access Explorer")

if page == "Detailed Metadata":
    st.header("📘 Detailed Metadata")
    df = load_data(METADATA_URL)

    # Cascading filters
    filtered_df = df.copy()
    def add_multiselect_filter(df, column_name, label=None):
        options = sorted(df[column_name].dropna().unique())
        label = label or column_name
        selection = st.multiselect(label, options)
        if selection:
            df = df[df[column_name].isin(selection)]
        return df

    for col in ["Platform", "Space", "Data Point", "MCL UI", "MCL API", "Brandwatch"]:
        if col in filtered_df.columns:
            filtered_df = add_multiselect_filter(filtered_df, col)

    for col in ["MCL UI", "MCL API", "Brandwatch"]:
        if col in filtered_df.columns:
            filtered_df[col] = filtered_df[col].apply(format_access)

else:
    st.header("📊 Topline Summary")
    df = load_data(TOPLINE_URL)
    df = df.set_index(df.columns[0])

    # Replace Y/N with icons (✅ / ❌) across the whole table
    df = df.applymap(lambda val: "✅" if val == "Y" else "❌" if val == "N" else val)

    # Filters
    access_types = df.index.tolist()
    access_filter = st.multiselect("Access Types", access_types, default=access_types)

    platform_options = df.columns.tolist()
    platform_filter = st.multiselect("Platforms", platform_options, default=platform_options)

    # Apply filters
    filtered_df = df.loc[access_filter, platform_filter]

    # Reset index to make access type a visible column
    filtered_df = filtered_df.reset_index()

# Show results
st.subheader(f"Filtered Results ({len(filtered_df)} rows)")
st.markdown("""
    <style>
    .stDataFrame td {
        white-space: normal !important;
        word-wrap: break-word !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.dataframe(filtered_df, use_container_width=True, height=700)

# Download
csv = filtered_df.to_csv(index=False)
st.download_button("Download Filtered Data as CSV", csv, f"{page.lower().replace(' ', '_')}_filtered.csv", "text/csv")
