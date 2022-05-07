import os

from flask import request             
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider   
from opentelemetry.sdk.resources import SERVICE_NAME, Resource     
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

from app.core import app, db, migrate
<<<<<<< HEAD
from app.views.oauth_view import oauth_blueprint
from app.views.sample_page import sample_page_blueprint
=======
from app.core.config import Config
>>>>>>> add adaptive rate. default 5% on test 100%
from app.views.user_view import user_blueprint
from app.views.role_view import role_blueprint
from app.views.user_add_role import user_role_blueprint
from app.views.auth_views import auth_blueprint


def create_app(flask_app):
    db.init_app(app=flask_app)
    flask_app.register_blueprint(role_blueprint)
    flask_app.register_blueprint(user_role_blueprint)
    flask_app.register_blueprint(user_blueprint)
    flask_app.register_blueprint(auth_blueprint)
    flask_app.register_blueprint(oauth_blueprint)
    flask_app.register_blueprint(sample_page_blueprint)
    migrate.init_app(app, db)

    return flask_app



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


configure_tracer()
app = create_app(app)
FlaskInstrumentor().instrument_app(app) 

@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required') 

if __name__ == "__main__":
    app.run(
        host=os.getenv('HOST', 'localhost'),
        debug=bool(os.getenv('DEBUG', 1)),
    )
