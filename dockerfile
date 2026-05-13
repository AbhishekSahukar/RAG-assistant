FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_HEADLESS=true

# Install minimal required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Create required directories
RUN mkdir -p vector_store

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/app.conf

# Expose Streamlit public port
EXPOSE 8501

# Start supervisor
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/app.conf"]