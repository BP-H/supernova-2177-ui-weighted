#!/bin/bash
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

# Launch the Streamlit UI
UI_FILE="ui.py"

if [[ ! -f "$UI_FILE" ]]; then
  echo "❌ $UI_FILE not found. Please ensure it exists." >&2
  exit 1
fi

# Listen on port 8888 by default. Set STREAMLIT_PORT or pass --server.port
# to override this value.
PORT="${STREAMLIT_PORT:-${PORT:-8888}}"

  echo "🚀 Launching Streamlit UI: $UI_FILE on port $PORT"
  # Pass through any additional args (e.g. --real-backend)
  streamlit run "$UI_FILE" \
    --server.headless true \
    --server.address 0.0.0.0 \
    --server.port "$PORT" \
    -- "$@"
