import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="World Clocks", layout="wide")
st.title("World Clocks")

ALL_CITIES = {
    "New York City":  {"tz": "America/New_York",    "flag": "🗽"},
    "Seoul":          {"tz": "Asia/Seoul",           "flag": "🇰🇷"},
    "Fremont":        {"tz": "America/Los_Angeles",  "flag": "🌉"},
    "London":         {"tz": "Europe/London",        "flag": "🇬🇧"},
    "Paris":          {"tz": "Europe/Paris",         "flag": "🗼"},
    "Tokyo":          {"tz": "Asia/Tokyo",           "flag": "🗾"},
    "Sydney":         {"tz": "Australia/Sydney",     "flag": "🦘"},
    "Dubai":          {"tz": "Asia/Dubai",           "flag": "🇦🇪"},
    "Singapore":      {"tz": "Asia/Singapore",       "flag": "🇸🇬"},
    "Chicago":        {"tz": "America/Chicago",      "flag": "🌆"},
    "Los Angeles":    {"tz": "America/Los_Angeles",  "flag": "🎬"},
    "Toronto":        {"tz": "America/Toronto",      "flag": "🍁"},
    "Berlin":         {"tz": "Europe/Berlin",        "flag": "🇩🇪"},
    "Mumbai":         {"tz": "Asia/Kolkata",         "flag": "🇮🇳"},
    "Beijing":        {"tz": "Asia/Shanghai",        "flag": "🇨🇳"},
}

if "active_cities" not in st.session_state:
    st.session_state.active_cities = ["New York City", "Seoul", "Fremont"]

# Controls row
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    available = [c for c in ALL_CITIES if c not in st.session_state.active_cities]
    selected = st.selectbox("Add a city", available, label_visibility="collapsed",
                            placeholder="Select a city to add...")
with col2:
    if st.button("Add Clock", type="primary", use_container_width=True):
        if selected and selected not in st.session_state.active_cities:
            st.session_state.active_cities.append(selected)
            st.rerun()
with col3:
    if st.button("Remove Last", use_container_width=True):
        if len(st.session_state.active_cities) > 1:
            st.session_state.active_cities.pop()
            st.rerun()

# Build clock data for JS
clocks_data = [
    {"id": c.lower().replace(" ", "_"),
     "city": c,
     "tz": ALL_CITIES[c]["tz"],
     "flag": ALL_CITIES[c]["flag"]}
    for c in st.session_state.active_cities
]
clocks_json = json.dumps(clocks_data)

components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{ background: transparent; margin: 0; padding: 0; font-family: monospace; }}
  #toolbar {{ text-align: right; margin-bottom: 8px; }}
  #toolbar button {{
    background: #3b3b5c; color: #ccc; border: none;
    border-radius: 8px; padding: 6px 14px; cursor: pointer; font-size: 13px;
  }}
  #canvas {{ position: relative; width: 100%; height: 520px; }}
  .clock {{
    position: absolute; width: 200px;
    background: #1e1e2e; border-radius: 16px;
    padding: 24px 20px; text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    cursor: grab; user-select: none;
    transition: box-shadow 0.15s;
  }}
  .clock:active {{ cursor: grabbing; box-shadow: 0 8px 32px rgba(0,0,0,0.6); }}
  .city  {{ font-size: 13px; color: #aaa; margin-bottom: 4px; letter-spacing: 1px; }}
  .time  {{ font-size: 38px; color: #f0f0f0; font-weight: bold; }}
  .date  {{ font-size: 11px; color: #666; margin-top: 6px; }}
  .flag  {{ font-size: 26px; margin-bottom: 4px; }}
</style>
</head>
<body>
<div id="toolbar">
  <button onclick="arrangeClocks()">⟳ Auto-arrange</button>
</div>
<div id="canvas"></div>

<script>
  const CLOCKS = {clocks_json};

  // Create clock elements
  const canvas = document.getElementById("canvas");
  CLOCKS.forEach(c => {{
    const el = document.createElement("div");
    el.className = "clock";
    el.id = "clock-" + c.id;
    el.innerHTML = `
      <div class="flag">${{c.flag}}</div>
      <div class="city">${{c.city.toUpperCase()}}</div>
      <div class="time" id="time-${{c.id}}">--:--:--</div>
      <div class="date" id="date-${{c.id}}"></div>
    `;
    canvas.appendChild(el);
    makeDraggable(el);
  }});

  // Update times
  function updateClocks() {{
    CLOCKS.forEach(c => {{
      const now = new Date();
      document.getElementById("time-" + c.id).textContent =
        now.toLocaleTimeString("en-US", {{ timeZone: c.tz, hour12: false }});
      document.getElementById("date-" + c.id).textContent =
        now.toLocaleDateString("en-US", {{
          timeZone: c.tz, weekday: "short", month: "short", day: "numeric", year: "numeric"
        }});
    }});
  }}
  updateClocks();
  setInterval(updateClocks, 1000);

  // Auto-arrange evenly
  function arrangeClocks() {{
    const canvasW = canvas.offsetWidth;
    const els = CLOCKS.map(c => document.getElementById("clock-" + c.id));
    const cw = els[0].offsetWidth;
    const ch = els[0].offsetHeight;
    const n = els.length;
    const perRow = Math.min(n, Math.floor(canvasW / (cw + 20)));
    const rows = Math.ceil(n / perRow);
    els.forEach((el, i) => {{
      const row = Math.floor(i / perRow);
      const col = i % perRow;
      const totalRowW = Math.min(n - row * perRow, perRow) * cw;
      const gap = (canvasW - totalRowW) / (Math.min(n - row * perRow, perRow) + 1);
      el.style.left = (gap + col * (cw + gap)) + "px";
      el.style.top = (20 + row * (ch + 30)) + "px";
    }});
  }}
  window.addEventListener("load", arrangeClocks);
  window.addEventListener("resize", arrangeClocks);

  // Drag
  function makeDraggable(el) {{
    let dragging = false, offX = 0, offY = 0;
    el.addEventListener("mousedown", e => {{
      dragging = true;
      const r = el.getBoundingClientRect();
      offX = e.clientX - r.left;
      offY = e.clientY - r.top;
      el.style.zIndex = 1000;
      e.preventDefault();
    }});
    document.addEventListener("mousemove", e => {{
      if (!dragging) return;
      const cr = canvas.getBoundingClientRect();
      let x = Math.max(0, Math.min(e.clientX - cr.left - offX, cr.width - el.offsetWidth));
      let y = Math.max(0, Math.min(e.clientY - cr.top - offY, cr.height - el.offsetHeight));
      el.style.left = x + "px";
      el.style.top  = y + "px";
    }});
    document.addEventListener("mouseup", () => {{ dragging = false; el.style.zIndex = ""; }});
  }}
</script>
</body>
</html>
""", height=580)
