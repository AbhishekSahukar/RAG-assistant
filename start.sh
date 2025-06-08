#!/bin/bash

echo "🟢 Starting FastAPI on port $PORT..."
uvicorn backend.main:app --host 0.0.0.0 --port $PORT &

echo "🟢 Starting Streamlit on port 8501..."
streamlit run frontend/app.py \
  --server.port=8501 \
  --server.address=0.0.0.0
