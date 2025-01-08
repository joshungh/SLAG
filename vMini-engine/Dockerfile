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

# Create all directories with proper permissions
RUN mkdir -p /app/output/stories /app/output/frameworks /app/logs /app/.pytest_cache && \
    chmod -R 777 /app/output /app/logs /app/.pytest_cache && \
    chown -R nobody:nogroup /app/output /app/logs /app/.pytest_cache

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

# Switch to non-root user
USER nobody

# Run the API service
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 

# After creating other directories
RUN mkdir -p /app/.pytest_cache && \
    chmod -R 777 /app/.pytest_cache 