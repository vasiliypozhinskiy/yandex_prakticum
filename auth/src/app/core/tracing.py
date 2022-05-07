from app.core.config import Config
from app.core import app

from flask import Blueprint, request         
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider   
from opentelemetry.sdk.resources import SERVICE_NAME, Resource     
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

tracing_blueprint = Blueprint("tracing", __name__)

def configure_tracer() -> None:
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: "auth"}),
            sampler=TraceIdRatioBased(Config.TRACE_SAMPLING_FREQUENCY)
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name='tracing',
                agent_port=6831,
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

@tracing_blueprint.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required') 