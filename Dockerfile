FROM python:3.10

WORKDIR /app

# Copy everything into the image
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure config is recognized
RUN mkdir -p /app/.streamlit
COPY .streamlit/config.toml /app/.streamlit/config.toml

# Expose the Streamlit port (used by Render)
EXPOSE 8501

# Run both apps
CMD ["bash", "start.sh"]
