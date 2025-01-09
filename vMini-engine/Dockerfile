# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and setup files
COPY requirements.txt setup.py ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src ./src

# Install local package
RUN pip install -e .

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app/src ./src
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/

# Create necessary directories with proper permissions
RUN mkdir -p /app/output/stories /app/output/frameworks /app/logs && \
    chmod -R 777 /app/output /app/logs && \
    chown -R nobody:nogroup /app/output /app/logs

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8000/health || exit 1

# Switch to non-root user
USER nobody

# Run the API service (no reload in production)
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 