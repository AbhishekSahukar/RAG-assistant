FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for PyMuPDF and faiss
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy app code
COPY backend /app/backend
COPY frontend /app/frontend
COPY requirements.txt /app/requirements.txt
COPY start.sh /app/start.sh

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Make start script executable
RUN chmod +x /app/start.sh

# Expose backend and frontend ports
EXPOSE 8000
EXPOSE 8501

# Start both backend and frontend
CMD ["sh", "/app/start.sh"]
