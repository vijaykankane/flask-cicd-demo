# Flask CI/CD Demo - Environment Configuration Example
# Copy this file to .env and customize the values for your environment
# IMPORTANT: Never commit .env files to version control

# ================================
# Flask Application Configuration
# ================================

# Flask Environment (development, staging, production, testing)
FLASK_ENV=development

# Enable/disable debug mode (true/false)
FLASK_DEBUG=true

# Secret key for session management (generate a secure random key for production)
SECRET_KEY=dev-secret-key-change-in-production-to-secure-random-string

# Application host and port
HOST=0.0.0.0
PORT=5000

# Application version and build information
BUILD_NUMBER=1
GIT_COMMIT=unknown
VERSION=1.0.0

# ================================
# Docker Configuration
# ================================

# Environment for docker-compose (dev, staging, prod)
ENV=dev

# Docker image tag
TAG=latest

# Build arguments
BUILD_DATE=2024-01-15T10:00:00Z
BUILD_VERSION=1.0.0

# ================================
# Gunicorn Configuration (Production)
# ================================

# Number of worker processes
GUNICORN_WORKERS=4

# Number of threads per worker
GUNICORN_THREADS=2

# Request timeout in seconds
GUNICORN_TIMEOUT=30

# Keep-alive connections
GUNICORN_KEEPALIVE=2

# Maximum requests per worker before restart
GUNICORN_MAX_REQUESTS=1000

# Jitter for max requests
GUNICORN_MAX_REQUESTS_JITTER=100

# ================================
# Database Configuration (Optional)
# ================================

# Database URL (SQLite example)
DATABASE_URL=sqlite:///app.db

# PostgreSQL example
# DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# MySQL example
# DATABASE_URL=mysql://username:password@localhost:3306/dbname

# Database pool settings
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# ================================
# Redis Configuration (Optional)
# ================================

# Redis connection URL
REDIS_URL=redis://localhost:6379/0

# Redis password (if required)
REDIS_PASSWORD=devpassword

# Redis key prefix
REDIS_KEY_PREFIX=flask-cicd-demo

# ================================
# Security Configuration
# ================================

# JWT Secret Key (if using JWT authentication)
JWT_SECRET_KEY=jwt-secret-key-change-in-production

# Session cookie configuration
SESSION_COOKIE_SECURE=false
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=Lax

# CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# ================================
# Email/SMTP Configuration
# ================================

# SMTP server configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Email addresses
EMAIL_FROM=noreply@company.com
EMAIL_TO=admin@company.com

# ================================
# Logging Configuration
# ================================

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Log format
LOG_FORMAT=[%(asctime)s] %(levelname)s in %(module)s: %(message)s

# Log file path
LOG_FILE=app.log

# Enable/disable file logging
LOG_TO_FILE=false

# ================================
# Monitoring and Metrics
# ================================

# Enable metrics collection
ENABLE_METRICS=true

# Metrics export port
METRICS_PORT=9090

# Health check endpoint path
HEALTH_CHECK_PATH=/health

# ================================
# External Services
# ================================

# API keys and external service URLs
# EXTERNAL_API_KEY=your-api-key-here
# EXTERNAL_SERVICE_URL=https://api.external-service.com

# Third-party service configuration
# ANALYTICS_TRACKING_ID=GA-12345678-1
# SENTRY_DSN=https://your-sentry-dsn@sentry.io/project

# ================================
# CI/CD Configuration
# ================================

# Docker registry configuration
DOCKER_REGISTRY=docker.io
DOCKER_REPOSITORY=your-username/flask-cicd-demo
DOCKER_USERNAME=your-dockerhub-username
# DOCKER_TOKEN=your-dockerhub-token  # Set in CI/CD secrets, not here

# Deployment targets
STAGING_HOST=staging.example.com
STAGING_PORT=5000
PRODUCTION_HOST=production.example.com
PRODUCTION_PORT=80

# Notification settings
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
SLACK_CHANNEL=#devops-alerts

# ================================
# Testing Configuration
# ================================

# Test database URL (separate from production)
TEST_DATABASE_URL=sqlite:///test.db

# Testing environment variables
TESTING=false
TEST_COVERAGE_THRESHOLD=80

# ================================
# Performance Configuration
# ================================

# Request timeout settings
REQUEST_TIMEOUT=30

# Rate limiting settings
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100

# Caching configuration
CACHE_TYPE=simple
CACHE_DEFAULT_TIMEOUT=300

# ================================
# Development Tools
# ================================

# Enable development tools
ENABLE_DEBUG_TOOLBAR=true

# Auto-reload on file changes
AUTO_RELOAD=true

# Profiling
ENABLE_PROFILING=false

# ================================
# Cloud Provider Configuration
# ================================

# AWS Configuration (if deploying to AWS)
# AWS_REGION=us-east-1
# AWS_ACCESS_KEY_ID=your-access-key
# AWS_SECRET_ACCESS_KEY=your-secret-key
# AWS_S3_BUCKET=your-s3-bucket

# Google Cloud Configuration (if deploying to GCP)
# GOOGLE_CLOUD_PROJECT=your-project-id
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Azure Configuration (if deploying to Azure)
# AZURE_SUBSCRIPTION_ID=your-subscription-id
# AZURE_RESOURCE_GROUP=your-resource-group

# ================================
# Custom Application Settings
# ================================

# Add any custom application-specific environment variables here
# CUSTOM_FEATURE_ENABLED=true
# MAX_UPLOAD_SIZE=16777216  # 16MB
# DEFAULT_PAGINATION_SIZE=20

# ================================
# Important Security Notes
# ================================

# 1. Never commit this file with real secrets to version control
# 2. Use strong, randomly generated keys for production
# 3. Rotate secrets regularly
# 4. Use environment-specific values
# 5. Consider using secret management services (AWS Secrets Manager, HashiCorp Vault, etc.)
# 6. Validate and sanitize all environment variables
# 7. Use different secrets for different environments

# ================================
# Environment-Specific Examples
# ================================

# Development Environment:
# FLASK_ENV=development
# FLASK_DEBUG=true
# SECRET_KEY=dev-secret-key
# DATABASE_URL=sqlite:///dev.db

# Staging Environment:
# FLASK_ENV=staging
# FLASK_DEBUG=false
# SECRET_KEY=staging-secret-key-random-string
# DATABASE_URL=postgresql://user:pass@staging-db:5432/dbname

# Production Environment:
# FLASK_ENV=production
# FLASK_DEBUG=false
# SECRET_KEY=production-super-secure-random-key
# DATABASE_URL=postgresql://user:pass@prod-db:5432/dbname