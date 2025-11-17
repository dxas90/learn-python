import os
import sys
import logging
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.environ.get("FLASK_ENV") == "development" else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS
CORS(app, origins=os.environ.get("CORS_ORIGIN", "*"))

# Application metadata
APP_INFO = {
    "name": "learn-python",
    "version": os.environ.get("APP_VERSION", "0.0.1"),
    "environment": os.environ.get("FLASK_ENV", "development"),
    "timestamp": datetime.now(timezone.utc).isoformat(),
}


# Middleware for logging
@app.before_request
def log_request():
    if os.environ.get("FLASK_ENV") != "test":
        user_agent = request.headers.get("User-Agent", "Unknown")
        logger.info(
            f"{request.method} {request.path} - User-Agent: {user_agent}"
        )


# Security headers middleware
@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return (
        jsonify(
            {
                "error": True,
                "message": "Resource not found",
                "statusCode": 404,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ),
        404,
    )


@app.errorhandler(500)
def internal_error(error):
    return (
        jsonify(
            {
                "error": True,
                "message": "Internal Server Error",
                "statusCode": 500,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "details": (
                    str(error) if os.environ.get("FLASK_ENV") != "production" else None
                ),
            }
        ),
        500,
    )


# Route: Welcome page
@app.route("/")
def index():
    """Welcome endpoint with API documentation"""
    welcome_data = {
        "message": "Welcome to learn-python API",
        "description": "A simple Flask microservice for learning and demonstration",
        "documentation": {"swagger": None, "postman": None},
        "links": {
            "repository": "https://github.com/dxas90/learn-python",
            "issues": "https://github.com/dxas90/learn-python/issues",
        },
        "endpoints": [
            {
                "path": "/",
                "method": "GET",
                "description": "API welcome and documentation",
            },
            {
                "path": "/ping",
                "method": "GET",
                "description": "Simple ping-pong response",
            },
            {
                "path": "/healthz",
                "method": "GET",
                "description": "Health check endpoint",
            },
            {
                "path": "/info",
                "method": "GET",
                "description": "Application and system information",
            },
            {
                "path": "/echo",
                "method": "POST",
                "description": "Echo back the request body",
            },
        ],
    }
    return jsonify(
        {
            "success": True,
            "data": welcome_data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


# Route: Ping
@app.route("/ping")
def ping():
    """Simple ping-pong response"""
    return "pong", 200, {"Content-Type": "text/plain"}


# Route: Health check
@app.route("/healthz")
def healthz():
    """Health check endpoint with basic information"""
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": APP_INFO["version"],
        "environment": APP_INFO["environment"],
    }

    return jsonify(
        {
            "success": True,
            "data": health_data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


# Route: Application info
@app.route("/info")
def info():
    """Application and system information endpoint"""
    system_info = {
        "application": APP_INFO,
        "system": {
            "python_version": sys.version,
        },
        "environment": {
            "python_env": os.environ.get("PYTHON_ENV", "Not set"),
            "flask_env": os.environ.get("FLASK_ENV", "development"),
            "port": os.environ.get("PORT", "8000"),
            "host": os.environ.get("HOST", "0.0.0.0"),
        },
    }

    return jsonify(
        {
            "success": True,
            "data": system_info,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


# Route: Echo (for testing POST requests)
@app.route("/echo", methods=["POST"])
def echo():
    """Echo back the request body"""
    try:
        data = request.get_json()
        return jsonify(
            {
                "success": True,
                "data": {
                    "echo": data,
                    "headers": dict(request.headers),
                    "method": request.method,
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
    except Exception:
        return (
            jsonify(
                {
                    "error": True,
                    "message": "Invalid JSON",
                    "statusCode": 400,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            ),
            400,
        )


# Route: Version
@app.route("/version")
def version():
    """Get application version"""
    return jsonify(
        {
            "success": True,
            "data": {
                "version": APP_INFO["version"],
                "name": APP_INFO["name"],
                "environment": APP_INFO["environment"],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("FLASK_ENV", "development") == "development"

    logger.info(f"🚀 Server starting at http://{host}:{port}/")
    logger.info(f"📊 Environment: {APP_INFO['environment']}")
    logger.info(f"📦 Version: {APP_INFO['version']}")
    logger.info(f"🕐 Started at: {APP_INFO['timestamp']}")

    app.run(host=host, port=port, debug=debug)
