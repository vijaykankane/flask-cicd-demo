#!/usr/bin/env python3
"""
Comprehensive test suite for Flask CI/CD Demo Application
Uses pytest framework for testing
"""

import pytest
import json
import os
import sys
from datetime import datetime

# Add the parent directory to the path to import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

class TestFlaskApplication:
    """Test suite for Flask application"""
    
    @pytest.fixture
    def app(self):
        """Create test application instance"""
        app = create_app('testing')
        app.config.update({
            'TESTING': True,
            'DEBUG': False,
            'SECRET_KEY': 'test-secret-key'
        })
        return app
    
    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    @pytest.fixture
    def runner(self, app):
        """Create test CLI runner"""
        return app.test_cli_runner()

class TestHomeEndpoint(TestFlaskApplication):
    """Test home page functionality"""
    
    def test_home_page_loads(self, client):
        """Test that home page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Flask CI/CD Demo Application' in response.data
    
    def test_home_page_contains_version(self, client):
        """Test that home page contains version information"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Version:' in response.data
        assert b'1.0.0' in response.data
    
    def test_home_page_contains_status(self, client):
        """Test that home page shows running status"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'RUNNING' in response.data
    
    def test_home_page_content_type(self, client):
        """Test home page returns HTML content type"""
        response = client.get('/')
        assert response.status_code == 200
        assert 'text/html' in response.content_type

class TestHealthEndpoint(TestFlaskApplication):
    """Test health check functionality"""
    
    def test_health_check_success(self, client):
        """Test health check returns 200 OK"""
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_health_check_json_format(self, client):
        """Test health check returns valid JSON"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert 'timestamp' in data
        assert 'version' in data
        assert data['status'] == 'healthy'
    
    def test_health_check_version(self, client):
        """Test health check includes correct version"""
        response = client.get('/health')
        data = json.loads(response.data)
        assert data['version'] == '1.0.0'
    
    def test_health_check_timestamp_format(self, client):
        """Test health check timestamp is in ISO format"""
        response = client.get('/health')
        data = json.loads(response.data)
        # Should be able to parse ISO timestamp
        datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))

class TestAPIEndpoints(TestFlaskApplication):
    """Test API endpoints functionality"""
    
    def test_api_status_endpoint(self, client):
        """Test /api/status endpoint"""
        response = client.get('/api/status')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        required_fields = ['application', 'status', 'version', 'environment', 'timestamp']
        for field in required_fields:
            assert field in data
        
        assert data['status'] == 'running'
        assert data['version'] == '1.0.0'
    
    def test_api_version_endpoint(self, client):
        """Test /api/version endpoint"""
        response = client.get('/api/version')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        required_fields = ['version', 'build_number', 'git_commit', 'python_version']
        for field in required_fields:
            assert field in data
        
        assert data['version'] == '1.0.0'
    
    def test_api_echo_post_valid_json(self, client):
        """Test /api/echo endpoint with valid JSON"""
        test_data = {'message': 'Hello, World!', 'number': 42}
        response = client.post('/api/echo',
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'echo' in data
        assert data['echo'] == test_data
        assert data['method'] == 'POST'
    
    def test_api_echo_post_empty_data(self, client):
        """Test /api/echo endpoint with empty data"""
        response = client.post('/api/echo',
                             data='{}',
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'echo' in data
        assert data['echo'] == {}
    
    def test_api_echo_post_no_content_type(self, client):
        """Test /api/echo endpoint without content type"""
        response = client.post('/api/echo', data='test')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'echo' in data
    
    def test_api_metrics_endpoint(self, client):
        """Test /api/metrics endpoint"""
        response = client.get('/api/metrics')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'application' in data
        assert 'timestamp' in data
        # System metrics might not be available in test environment
        assert data['application']['version'] == '1.0.0'

class TestErrorHandling(TestFlaskApplication):
    """Test error handling functionality"""
    
    def test_404_error_handling(self, client):
        """Test 404 error returns proper JSON response"""
        response = client.get('/nonexistent-endpoint')
        assert response.status_code == 404
        data = json.loads(response.data)
        
        assert 'error' in data
        assert 'message' in data
        assert 'status_code' in data
        assert 'timestamp' in data
        assert data['status_code'] == 404
        assert data['error'] == 'Not Found'
    
    def test_405_method_not_allowed(self, client):
        """Test 405 error for wrong HTTP method"""
        # POST to health endpoint which only accepts GET
        response = client.post('/health')
        assert response.status_code == 405

class TestSecurityAndValidation(TestFlaskApplication):
    """Test security and validation features"""
    
    def test_api_echo_with_large_payload(self, client):
        """Test API echo with large JSON payload"""
        large_data = {'data': 'x' * 10000}  # 10KB of data
        response = client.post('/api/echo',
                             data=json.dumps(large_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['echo']['data'] == 'x' * 10000
    
    def test_api_echo_with_special_characters(self, client):
        """Test API echo with special characters"""
        test_data = {
            'special_chars': '!@#$%^&*()_+-=[]{}|;:,.<>?',
            'unicode': 'Hello 🌍 World 🚀',
            'quotes': 'He said "Hello" and \'Goodbye\''
        }
        response = client.post('/api/echo',
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['echo'] == test_data

class TestApplicationConfiguration(TestFlaskApplication):
    """Test application configuration"""
    
    def test_app_version_configuration(self, app):
        """Test application version is properly configured"""
        assert app.config['VERSION'] == '1.0.0'
    
    def test_app_testing_mode(self, app):
        """Test application is in testing mode"""
        assert app.config['TESTING'] is True
    
    def test_app_debug_mode_disabled(self, app):
        """Test debug mode is disabled in testing"""
        assert app.config['DEBUG'] is False

class TestIntegration(TestFlaskApplication):
    """Integration tests"""
    
    def test_full_workflow_simulation(self, client):
        """Simulate a full workflow: home -> health -> status -> echo"""
        # 1. Check home page
        response = client.get('/')
        assert response.status_code == 200
        
        # 2. Check health
        response = client.get('/health')
        assert response.status_code == 200
        health_data = json.loads(response.data)
        assert health_data['status'] == 'healthy'
        
        # 3. Check API status
        response = client.get('/api/status')
        assert response.status_code == 200
        status_data = json.loads(response.data)
        assert status_data['status'] == 'running'
        
        # 4. Test echo with workflow data
        echo_payload = {
            'workflow': 'integration_test',
            'timestamp': datetime.utcnow().isoformat(),
            'health_status': health_data['status'],
            'app_status': status_data['status']
        }
        
        response = client.post('/api/echo',
                             data=json.dumps(echo_payload),
                             content_type='application/json')
        assert response.status_code == 200
        echo_data = json.loads(response.data)
        assert echo_data['echo'] == echo_payload

# Performance tests (basic)
class TestPerformance(TestFlaskApplication):
    """Basic performance tests"""
    
    def test_health_endpoint_response_time(self, client):
        """Test health endpoint responds quickly"""
        import time
        start_time = time.time()
        response = client.get('/health')
        end_time = time.time()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        assert response_time < 1.0  # Should respond in less than 1 second
    
    def test_multiple_concurrent_requests(self, client):
        """Test handling multiple requests"""
        responses = []
        for i in range(10):
            response = client.get('/api/status')
            responses.append(response)
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'running'

# Pytest configuration and fixtures
@pytest.fixture(scope='session')
def app_config():
    """Session-wide application configuration"""
    return {
        'TESTING': True,
        'DEBUG': False,
        'SECRET_KEY': 'test-secret-key-for-session'
    }

def test_environment_variables():
    """Test that environment variables are properly handled"""
    # Test default values when env vars are not set
    app = create_app()
    assert app.config['PORT'] == 5000
    assert app.config['HOST'] == '0.0.0.0'

def test_application_factory():
    """Test application factory pattern"""
    app1 = create_app('testing')
    app2 = create_app('default')
    
    # Both should be Flask applications but separate instances
    assert app1 is not app2
    assert hasattr(app1, 'config')
    assert hasattr(app2, 'config')

if __name__ == '__main__':
    # Run tests directly
    pytest.main([__file__, '-v', '--tb=short'])