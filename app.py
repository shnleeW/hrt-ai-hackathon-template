import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="CSU Campus Map", layout="wide")

st.title("🎓 CSU Campus Locations")
st.write("Explore all 23 California State University campuses across California.")

@st.cache_data
def load_data():
    return pd.read_csv("data_ai/csu_campuses_geocoded.csv")

df = load_data()

# --- Sidebar filters ---
with st.sidebar:
    st.header("🔍 Filter Campuses")

    search = st.text_input("Search by name or city", placeholder="e.g. San Diego")

    cities = sorted(df["city"].unique())
    selected_cities = st.multiselect("Filter by city", options=cities)

    st.markdown("---")
    st.caption(f"{len(df)} campuses total")

# Apply filters
filtered = df.copy()
if search:
    mask = (
        filtered["campus"].str.contains(search, case=False, na=False) |
        filtered["city"].str.contains(search, case=False, na=False)
    )
    filtered = filtered[mask]
if selected_cities:
    filtered = filtered[filtered["city"].isin(selected_cities)]

# --- Summary metrics ---
col1, col2 = st.columns(2)
col1.metric("Campuses shown", len(filtered))
col2.metric("Cities represented", filtered["city"].nunique())

st.markdown("---")

# --- Map ---
center_lat = filtered["lat"].mean() if not filtered.empty else 36.7783
center_lon = filtered["lon"].mean() if not filtered.empty else -119.4179

m = folium.Map(location=[center_lat, center_lon], zoom_start=6, tiles="CartoDB positron")

for _, row in filtered.iterrows():
    popup_html = f"""
    <div style="font-family: sans-serif; min-width: 180px;">
        <b style="font-size:14px;">{row['campus']}</b><br>
        <hr style="margin:4px 0;">
        📍 {row['street_address']}<br>
        {row['city']}, {row['state']} {row['zip']}
    </div>
    """
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=row["campus"],
        icon=folium.Icon(color="darkblue", icon="graduation-cap", prefix="fa"),
    ).add_to(m)

st_folium(m, width="100%", height=520, returned_objects=[])

st.markdown("---")

# --- Data table ---
st.subheader("📋 Campus Directory")
display_df = filtered[["campus", "street_address", "city", "state", "zip"]].rename(columns={
    "campus": "Campus",
    "street_address": "Address",
    "city": "City",
    "state": "State",
    "zip": "ZIP"
}).reset_index(drop=True)

st.dataframe(display_df, use_container_width=True, hide_index=True)
