# 🌍 World Clock Monitor

A live dashboard that displays the current time across multiple cities around the world, all in one place.

## What It Does

- **Live clock cards** — Shows the current time, date, and UTC offset for 12 major global cities in a clean, easy-to-read card grid
- **Customizable city list** — Add any city from hundreds of available timezones or remove cities you don't need, with a one-click reset to defaults
- **Auto-refresh mode** — Toggle automatic page refresh every 60 seconds to keep all clocks up to date without reloading manually

## How to Use

1. **Open the app** — The dashboard loads with 12 pre-selected cities (New York, London, Tokyo, Sydney, and more)
2. **Read the clocks** — Each card shows the city name, current local time, today's date, and its UTC offset
3. **Add a city** — Open the sidebar on the left, type a city name, choose its timezone from the dropdown, and click "Add City"
4. **Remove a city** — In the sidebar, select the city you want to remove from the dropdown and click "Remove City"
5. **Reset** — Click "Reset to Defaults" in the sidebar to restore the original 12 cities
6. **Keep it live** — Toggle "Auto-refresh" in the sidebar to have the page update automatically every 60 seconds

## Data

This app does not use any external datasets. All times are calculated in real time from your system clock using standard timezone definitions (IANA timezone database via the `pytz` library).

## Built With

- [Streamlit](https://streamlit.io) — Web app framework
- [Pandas](https://pandas.pydata.org) — Data table display
- [pytz](https://pythonhosted.org/pytz/) — Timezone conversion
- [datetime](https://docs.python.org/3/library/datetime.html) — Python standard library for time handling
