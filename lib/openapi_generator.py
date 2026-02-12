from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin


def generate_openapi_spec():
    """Generate OpenAPI spec from Flask app routes"""

    # Initialize APISpec
    spec = APISpec(
        title="Learn-Python API",
        version="0.0.1",
        openapi_version="3.0.0",
        info=dict(
            description="A simple Flask microservice for learning and demonstration"
        ),
        servers=[{"url": "http://localhost:8000", "description": "Local server"}],
        plugins=[FlaskPlugin()],
    )

    # Add paths manually for all endpoints
    spec.path(
        path="/",
        operations=dict(
            get=dict(
                summary="Welcome and API documentation",
                operationId="getWelcome",
                responses={
                    "200": {
                        "description": "Welcome message with API endpoints",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {"type": "object"},
                                        "timestamp": {"type": "string"},
                                    },
                                }
                            }
                        },
                    }
                },
            )
        ),
    )

    spec.path(
        path="/ping",
        operations=dict(
            get=dict(
                summary="Health check ping endpoint",
                operationId="getPing",
                responses={
                    "200": {
                        "description": "Pong response",
                        "content": {"text/plain": {"schema": {"type": "string"}}},
                    }
                },
            )
        ),
    )

    spec.path(
        path="/healthz",
        operations=dict(
            get=dict(
                summary="Detailed health check",
                operationId="getHealthz",
                responses={
                    "200": {
                        "description": "Health status with system metrics",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {"type": "object"},
                                        "timestamp": {"type": "string"},
                                    },
                                }
                            }
                        },
                    }
                },
            )
        ),
    )

    spec.path(
        path="/info",
        operations=dict(
            get=dict(
                summary="Application and system information",
                operationId="getInfo",
                responses={
                    "200": {
                        "description": "Detailed system and application info",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {"type": "object"},
                                        "timestamp": {"type": "string"},
                                    },
                                }
                            }
                        },
                    }
                },
            )
        ),
    )

    spec.path(
        path="/version",
        operations=dict(
            get=dict(
                summary="Application version",
                operationId="getVersion",
                responses={
                    "200": {
                        "description": "Application version information",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {"type": "object"},
                                        "timestamp": {"type": "string"},
                                    },
                                }
                            }
                        },
                    }
                },
            )
        ),
    )

    spec.path(
        path="/echo",
        operations=dict(
            post=dict(
                summary="Echo request body",
                operationId="postEcho",
                requestBody={
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"type": "object", "additionalProperties": True}
                        }
                    },
                },
                responses={
                    "200": {
                        "description": "Echoed request data with headers",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {"type": "object"},
                                        "timestamp": {"type": "string"},
                                    },
                                }
                            }
                        },
                    },
                    "400": {"description": "Invalid JSON"},
                },
            )
        ),
    )

    spec.path(
        path="/metrics",
        operations=dict(
            get=dict(
                summary="Prometheus metrics endpoint",
                operationId="getMetrics",
                responses={
                    "200": {
                        "description": "Prometheus metrics in text format",
                        "content": {"text/plain": {"schema": {"type": "string"}}},
                    }
                },
            )
        ),
    )

    return spec.to_dict()
