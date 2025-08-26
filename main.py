from fastapi import FastAPI
import logging
import os
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# Logging
logging.basicConfig(
    filename="/var/log/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Tracing
resource = Resource.create({
    "service.name": "fastapi-app",
    "service.namespace": "demo",
    "service.version": "1.0.0",
})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://tempo:4317")
otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

app = FastAPI()

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    logging.info("Root endpoint was called")
    with tracer.start_as_current_span("root-handler"):
        return {"message": "Hello Monitoring!"}
