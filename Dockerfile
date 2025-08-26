# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenTelemetry auto-instrumentation
RUN pip install --no-cache-dir opentelemetry-distro opentelemetry-exporter-otlp

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Run app with OTel instrumentation
CMD ["opentelemetry-instrument", \
     "--traces_exporter", "otlp", \
     "--metrics_exporter", "none", \
     "--logs_exporter", "none", \
     "--service_name", "fastapi-app", \
     "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
