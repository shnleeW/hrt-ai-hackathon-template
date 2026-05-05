import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

st.set_page_config(page_title="World Clock Monitor", layout="wide")

st.title("🌍 World Clock Monitor")
st.write("Track the current time across multiple cities around the world.")

# Default cities with timezones
DEFAULT_CITIES = [
    ("New York", "America/New_York"),
    ("London", "Europe/London"),
    ("Paris", "Europe/Paris"),
    ("Dubai", "Asia/Dubai"),
    ("Tokyo", "Asia/Tokyo"),
    ("Sydney", "Australia/Sydney"),
    ("Los Angeles", "America/Los_Angeles"),
    ("Chicago", "America/Chicago"),
    ("São Paulo", "America/Sao_Paulo"),
    ("Singapore", "Asia/Singapore"),
    ("Hong Kong", "Asia/Hong_Kong"),
    ("Mumbai", "Asia/Kolkata"),
]

# All available timezones for the selector
all_timezones = sorted(pytz.all_timezones)

# Session state for custom cities
if "cities" not in st.session_state:
    st.session_state.cities = list(DEFAULT_CITIES)

# Sidebar: add/remove cities
with st.sidebar:
    st.header("Manage Cities")

    st.subheader("Add a City")
    new_city = st.text_input("City Name", placeholder="e.g. Berlin")
    new_tz = st.selectbox("Timezone", all_timezones, index=all_timezones.index("Europe/Berlin"))
    if st.button("Add City", use_container_width=True):
        if new_city.strip():
            st.session_state.cities.append((new_city.strip(), new_tz))
            st.success(f"Added {new_city.strip()}")
        else:
            st.warning("Please enter a city name.")

    st.divider()
    st.subheader("Remove a City")
    city_names = [c[0] for c in st.session_state.cities]
    remove_city = st.selectbox("Select city to remove", city_names)
    if st.button("Remove City", use_container_width=True):
        st.session_state.cities = [c for c in st.session_state.cities if c[0] != remove_city]
        st.success(f"Removed {remove_city}")

    st.divider()
    if st.button("Reset to Defaults", use_container_width=True):
        st.session_state.cities = list(DEFAULT_CITIES)

    st.divider()
    auto_refresh = st.toggle("Auto-refresh (every 60s)", value=False)
    if auto_refresh:
        st.caption("Page will refresh every 60 seconds.")

# Build clock data
now_utc = datetime.now(pytz.utc)
rows = []
for city, tz_name in st.session_state.cities:
    tz = pytz.timezone(tz_name)
    local_time = now_utc.astimezone(tz)
    offset = local_time.utcoffset().total_seconds() / 3600
    rows.append({
        "City": city,
        "Time": local_time.strftime("%I:%M %p"),
        "Date": local_time.strftime("%a, %b %d %Y"),
        "Timezone": tz_name,
        "UTC Offset": f"UTC{offset:+.1f}".replace(".0", ""),
    })

df = pd.DataFrame(rows)

# Reference time
st.caption(f"Reference UTC time: {now_utc.strftime('%Y-%m-%d %H:%M:%S')} UTC")

# Display clocks as cards in a grid
st.subheader("Current Times")
cols_per_row = 4
cities_list = st.session_state.cities

for i in range(0, len(rows), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, col in enumerate(cols):
        idx = i + j
        if idx < len(rows):
            row = rows[idx]
            with col:
                st.markdown(f"""
<div style="background:#1e1e2e;border-radius:12px;padding:18px 16px 14px;text-align:center;margin-bottom:8px;">
    <div style="font-size:13px;color:#aaa;margin-bottom:4px;">{row['City']}</div>
    <div style="font-size:36px;font-weight:700;color:#fff;letter-spacing:2px;">{row['Time']}</div>
    <div style="font-size:12px;color:#ccc;margin-top:4px;">{row['Date']}</div>
    <div style="font-size:11px;color:#888;margin-top:6px;">{row['UTC Offset']}</div>
</div>
""", unsafe_allow_html=True)

# Table view
st.subheader("All Clocks — Table View")
st.dataframe(df, use_container_width=True, hide_index=True)

# Auto-refresh
if auto_refresh:
    import time
    time.sleep(60)
    st.rerun()
