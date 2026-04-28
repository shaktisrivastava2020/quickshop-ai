# QuickShop AI - Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Cloud Run uses PORT env var (default 8080)
ENV PORT=8080
EXPOSE 8080

# Run with gunicorn for production (multiple workers)
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1
