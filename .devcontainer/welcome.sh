#!/usr/bin/env bash
# Wait until the Claude Code extension is installed before printing the ready signal.

EXT_DIR="$HOME/.vscode-remote/extensions"
[ ! -d "$EXT_DIR" ] && EXT_DIR="$HOME/.vscode-server/extensions"

echo ""
echo "⏳ Setting up your workspace... (this can take up to a minute)"

for i in {1..60}; do
  if ls "$EXT_DIR"/anthropic.claude-code-* >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

clear
cat <<'EOF'

🎉 Hello! Welcome to the HRT Applied Research Hackathon! 🎉

✅ Everything is ready. Your workspace is set up.

👉 Step 1: Click the Claude (orange star) icon at the top right corner.
👉 Step 2: Sign in with your Claude Team account.
👉 Step 3: Ask Claude to build your app!

See README.md for the full list of helpful commands.

EOF
