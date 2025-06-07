FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# ✅ Expose only Streamlit's port
EXPOSE 8501

# ✅ Start script
CMD ["bash", "start.sh"]
