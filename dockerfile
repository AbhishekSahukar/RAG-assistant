FROM python:3.11-slim


RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


RUN python -c "from fastembed import TextEmbedding; TextEmbedding('sentence-transformers/all-MiniLM-L6-v2')"


COPY . .


RUN mkdir -p vector_store

COPY supervisord.conf /etc/supervisor/conf.d/app.conf

# Streamlit is the public-facing port
EXPOSE 8501

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/app.conf"]