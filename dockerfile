# Multi-stage Docker build for Flask CI/CD Demo Application
# This Dockerfile implements security best practices and optimization techniques
# suitable for enterprise production environments

# ================================
# Stage 1: Builder (Dependencies)
# ================================
FROM python:3.9-slim as builder

# Build arguments for metadata
ARG BUILD_DATE
ARG BUILD_VERSION
ARG VCS_REF

# Set build environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create build directory
WORKDIR /build

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt

# ================================
# Stage 2: Runtime Environment
# ================================
FROM python:3.9-slim as runtime

# Build arguments for metadata
ARG BUILD_DATE
ARG BUILD_VERSION="1.0.0"
ARG VCS_REF

# Add metadata labels (OCI Image Format Specification)
LABEL org.opencontainers.image.title="Flask CI/CD Demo Application" \
      org.opencontainers.image.description="Production-ready Flask application with comprehensive CI/CD pipeline" \
      org.opencontainers.image.version="${BUILD_VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.vendor="Enterprise DevOps Team" \
      org.opencontainers.image.authors="devops@company.com" \
      org.opencontainers.image.url="https://github.com/your-username/flask-cicd-demo" \
      org.opencontainers.image.source="https://github.com/your-username/flask-cicd-demo" \
      org.opencontainers.image.licenses="MIT"

# Install runtime dependencies and security updates
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    dumb-init \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r flask --gid=1000 && \
    useradd -r -g flask --uid=1000 --home-dir=/app --shell=/sbin/nologin \
    --comment "Flask application user" flask

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PATH=/home/flask/.local/bin:$PATH \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000 \
    GUNICORN_WORKERS=4 \
    GUNICORN_THREADS=2 \
    GUNICORN_TIMEOUT=30 \
    GUNICORN_KEEPALIVE=2 \
    GUNICORN_MAX_REQUESTS=1000 \
    GUNICORN_MAX_REQUESTS_JITTER=100

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/flask/.local

# Create application directory with proper permissions
WORKDIR /app
RUN chown -R flask:flask /app

# Copy application code with proper ownership
COPY --chown=flask:flask app.py .
COPY --chown=flask:flask requirements.txt .

# Copy additional configuration files if they exist
COPY --chown=flask:flask gunicorn.conf.py* ./

# Create gunicorn configuration if not provided
RUN if [ ! -f gunicorn.conf.py ]; then \
    cat > gunicorn.conf.py << 'EOF'
import os
import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'gevent'
worker_connections = 1000
max_requests = int(os.environ.get('GUNICORN_MAX_REQUESTS', 1000))
max_requests_jitter = int(os.environ.get('GUNICORN_MAX_REQUESTS_JITTER', 100))
timeout = int(os.environ.get('GUNICORN_TIMEOUT', 30))
keepalive = int(os.environ.get('GUNICORN_KEEPALIVE', 2))

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'flask-cicd-demo'

# Server mechanics
preload_app = True
daemon = False
pidfile = '/tmp/gunicorn.pid'
user = 1000
group = 1000
tmp_upload_dir = None

# SSL (if certificates are provided)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'
EOF
fi

# Switch to non-root user
USER flask

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Expose application port
EXPOSE 5000

# Set up proper signal handling and process management
ENTRYPOINT ["dumb-init", "--"]

# Production command using Gunicorn
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]

# Development/Debug command (can be overridden)
# CMD ["python", "app.py"]

# Security and optimization notes:
# 1. Multi-stage build reduces final image size
# 2. Non-root user (flask:1000) for security
# 3. dumb-init for proper signal handling
# 4. Health check for container orchestration
# 5. Gunicorn for production WSGI server
# 6. Environment variables for configuration
# 7. Proper file permissions and ownership
# 8. Security updates during build
# 9. Minimal base image (python:3.9-slim)
# 10. Build-time arguments for metadata