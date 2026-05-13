FROM python:3.11-slim

# Install supervisor for process management
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies before copying full source
# (takes advantage of Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Pre-create the vector store directory so it persists across restarts
RUN mkdir -p vector_store

# Supervisor config is copied from the repo root
COPY supervisord.conf /etc/supervisor/conf.d/app.conf

# Streamlit is the public-facing port
EXPOSE 8501

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/app.conf"]