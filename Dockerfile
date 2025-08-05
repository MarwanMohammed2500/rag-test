# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    supervisor && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports for Streamlit apps
EXPOSE 8501 8502

# Command to run supervisor
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]


# # Build the image
# docker build -t rag-app .

# # Run the container
# docker run -p 8501:8501 -p 8502:8502 rag-app
