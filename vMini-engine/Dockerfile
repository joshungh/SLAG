FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create output and logs directories
RUN mkdir -p /app/output /app/logs && \
    chmod 777 /app/output /app/logs

# Copy requirements and setup files first
COPY requirements.txt setup.py ./

# Copy the source code
COPY src ./src

# Install Python packages and the local package
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install -e .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the API service
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 