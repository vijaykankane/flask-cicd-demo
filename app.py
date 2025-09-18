#!/usr/bin/env python3
"""
Production-ready Flask Application for CI/CD Pipeline Demo
Author: Enterprise DevOps Team
Version: 1.0.0
"""

import os
import logging
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
import json
from functools import wraps
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application factory pattern
def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Configuration
    app.config.update({
        'SECRET_KEY': os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
        'DEBUG': os.environ.get('FLASK_DEBUG', 'False').lower() == 'true',
        'TESTING': os.environ.get('FLASK_TESTING', 'False').lower() == 'true',
        'PORT': int(os.environ.get('PORT', 5000)),
        'HOST': os.environ.get('HOST', '0.0.0.0'),
        'ENV': os.environ.get('FLASK_ENV', 'production'),
        'VERSION': '1.0.0',
        'BUILD_NUMBER': os.environ.get('BUILD_NUMBER', 'unknown'),
        'GIT_COMMIT': os.environ.get('GIT_COMMIT', 'unknown')
    })
    
    # Request logging middleware
    @app.before_request
    def log_request_info():
        logger.info(f"Request: {request.method} {request.url} - IP: {request.remote_addr}")
        request.start_time = time.time()
    
    @app.after_request
    def log_response_info(response):
        duration = time.time() - request.start_time
        logger.info(f"Response: {response.status_code} - Duration: {duration:.3f}s")
        return response
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status_code': 404,
            'timestamp': datetime.utcnow().isoformat()
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status_code': 500,
            'timestamp': datetime.utcnow().isoformat()
        }), 500
    
    # Rate limiting decorator
    def rate_limit(max_requests=100):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Simple in-memory rate limiting (use Redis in production)
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    # Routes
    @app.route('/')
    @rate_limit(max_requests=1000)
    def home():
        """Home page with application information"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Flask CI/CD Demo App</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .header { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
                .info-box { background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 10px 0; }
                .status-ok { color: #27ae60; font-weight: bold; }
                .build-info { background-color: #e8f4fd; border-left: 4px solid #3498db; padding: 10px; margin: 10px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="header">🚀 Flask CI/CD Demo Application</h1>
                <div class="info-box">
                    <h3>Application Status: <span class="status-ok">✅ RUNNING</span></h3>
                    <p><strong>Version:</strong> {{ version }}</p>
                    <p><strong>Environment:</strong> {{ env }}</p>
                    <p><strong>Current Time:</strong> {{ current_time }}</p>
                </div>
                
                <div class="build-info">
                    <h4>Build Information</h4>
                    <p><strong>Build Number:</strong> {{ build_number }}</p>
                    <p><strong>Git Commit:</strong> {{ git_commit }}</p>
                    <p><strong>Host:</strong> {{ host }}:{{ port }}</p>
                </div>
                
                <h3>Available Endpoints:</h3>
                <ul>
                    <li><code>GET /</code> - This home page</li>
                    <li><code>GET /health</code> - Health check endpoint</li>
                    <li><code>GET /api/status</code> - Application status (JSON)</li>
                    <li><code>GET /api/version</code> - Version information (JSON)</li>
                    <li><code>POST /api/echo</code> - Echo service for testing</li>
                    <li><code>GET /api/metrics</code> - Application metrics</li>
                </ul>
            </div>
        </body>
        </html>
        """
        
        return render_template_string(html_template,
            version=app.config['VERSION'],
            env=app.config['ENV'],
            current_time=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
            build_number=app.config['BUILD_NUMBER'],
            git_commit=app.config['GIT_COMMIT'],
            host=app.config['HOST'],
            port=app.config['PORT']
        )
    
    @app.route('/health')
    @rate_limit(max_requests=10000)
    def health_check():
        """Kubernetes/Docker health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': app.config['VERSION'],
            'uptime': 'Available'  # In production, track actual uptime
        }), 200
    
    @app.route('/api/status')
    @rate_limit(max_requests=1000)
    def api_status():
        """Detailed application status"""
        return jsonify({
            'application': 'Flask CI/CD Demo',
            'status': 'running',
            'version': app.config['VERSION'],
            'environment': app.config['ENV'],
            'build_number': app.config['BUILD_NUMBER'],
            'git_commit': app.config['GIT_COMMIT'],
            'timestamp': datetime.utcnow().isoformat(),
            'debug_mode': app.config['DEBUG'],
            'testing_mode': app.config['TESTING']
        })
    
    @app.route('/api/version')
    @rate_limit(max_requests=1000)
    def api_version():
        """Version information endpoint"""
        return jsonify({
            'version': app.config['VERSION'],
            'build_number': app.config['BUILD_NUMBER'],
            'git_commit': app.config['GIT_COMMIT'],
            'python_version': os.sys.version,
            'flask_version': Flask.__version__
        })
    
    @app.route('/api/echo', methods=['POST'])
    @rate_limit(max_requests=100)
    def api_echo():
        """Echo service for testing POST requests"""
        try:
            data = request.get_json() or {}
            return jsonify({
                'echo': data,
                'method': request.method,
                'content_type': request.content_type,
                'timestamp': datetime.utcnow().isoformat(),
                'headers': dict(request.headers)
            })
        except Exception as e:
            logger.error(f"Echo endpoint error: {e}")
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/metrics')
    @rate_limit(max_requests=100)
    def api_metrics():
        """Application metrics endpoint"""
        import psutil
        import sys
        
        try:
            return jsonify({
                'system': {
                    'cpu_percent': psutil.cpu_percent(),
                    'memory_percent': psutil.virtual_memory().percent,
                    'disk_usage': psutil.disk_usage('/').percent
                },
                'application': {
                    'version': app.config['VERSION'],
                    'environment': app.config['ENV'],
                    'python_version': sys.version,
                    'process_id': os.getpid()
                },
                'timestamp': datetime.utcnow().isoformat()
            })
        except ImportError:
            # Fallback if psutil is not available
            return jsonify({
                'system': 'metrics unavailable - psutil not installed',
                'application': {
                    'version': app.config['VERSION'],
                    'environment': app.config['ENV'],
                    'python_version': sys.version,
                    'process_id': os.getpid()
                },
                'timestamp': datetime.utcnow().isoformat()
            })
    
    return app

# Application instance
app = create_app()

if __name__ == '__main__':
    port = app.config['PORT']
    host = app.config['HOST']
    debug = app.config['DEBUG']
    
    logger.info(f"Starting Flask application on {host}:{port}")
    logger.info(f"Environment: {app.config['ENV']}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(host=host, port=port, debug=debug, threaded=True)