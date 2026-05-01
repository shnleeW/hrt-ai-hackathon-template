Run the Streamlit app and give the user a direct, clickable link.

Steps:
1. Check if streamlit is already running: `pgrep -f "streamlit run"`
   - If already running: skip the start step
   - If not running: run `streamlit run app.py --server.headless true &` to start it in the background
2. Wait 3 seconds for the server to start: `sleep 3`
3. Determine the URL:
   - If `$CODESPACE_NAME` is set (running in GitHub Codespace), the URL is:
     `https://${CODESPACE_NAME}-8501.app.github.dev`
   - Otherwise (running locally), the URL is:
     `http://localhost:8501`
4. Tell the user — print the URL on its own line so VS Code makes it clickable:

```
✅ Your app is running. Click the link below to open it:

<URL>
```

Do NOT tell the user about ports, sidebars, or globe icons. Just give the link.
