#!/bin/bash

echo "🌐 Starting Streamlit frontend on port 8501..."
streamlit run app.py \
  --server.port=8501 \
  --server.address=0.0.0.0
