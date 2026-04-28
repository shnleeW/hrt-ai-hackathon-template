import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import time

st.set_page_config(page_title="World Clocks", layout="wide")

st.title("World Clocks")

CITIES = {
    "New York City": "America/New_York",
    "Seoul": "Asia/Seoul",
    "Fremont": "America/Los_Angeles",
}

def get_time(tz_name):
    tz = pytz.timezone(tz_name)
    now = datetime.now(tz)
    return now.strftime("%H:%M:%S"), now.strftime("%A, %b %d %Y")

cols = st.columns(3)

for col, (city, tz) in zip(cols, CITIES.items()):
    current_time, current_date = get_time(tz)
    with col:
        st.markdown(
            f"""
            <div style="
                background-color: #1e1e2e;
                border-radius: 16px;
                padding: 32px 24px;
                text-align: center;
                box-shadow: 0 4px 16px rgba(0,0,0,0.3);
            ">
                <div style="font-size: 20px; color: #aaa; margin-bottom: 8px;">{city}</div>
                <div style="font-size: 56px; font-family: monospace; color: #f0f0f0; font-weight: bold;">{current_time}</div>
                <div style="font-size: 14px; color: #888; margin-top: 8px;">{current_date}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

time.sleep(1)
st.rerun()
