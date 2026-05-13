FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install only minimal required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt .

# Upgrade pip + install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create required folders
RUN mkdir -p vector_store

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/app.conf

# Expose Streamlit port
EXPOSE 8501

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/app.conf"]