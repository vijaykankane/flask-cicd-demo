# 🚀 Flask CI/CD Demo Application

[![CI/CD Pipeline](https://github.com/your-username/flask-cicd-demo/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/your-username/flask-cicd-demo/actions/workflows/ci-cd.yml)
[![Coverage](https://codecov.io/gh/your-username/flask-cicd-demo/branch/main/graph/badge.svg)](https://codecov.io/gh/your-username/flask-cicd-demo)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=flask-cicd-demo&metric=security_rating)](https://sonarcloud.io/dashboard?id=flask-cicd-demo)
[![Docker Pulls](https://img.shields.io/docker/pulls/your-username/flask-cicd-demo.svg)](https://hub.docker.com/r/your-username/flask-cicd-demo)

## 📋 Project Overview

This is a production-ready Flask web application demonstrating enterprise-grade CI/CD practices with both **Jenkins** and **GitHub Actions** pipelines. The project showcases automated testing, security scanning, containerization, and deployment strategies suitable for large-scale applications.

### 🎯 Key Features

- **🏗️ Production-Ready Flask App** - RESTful API with comprehensive endpoints
- **🧪 Comprehensive Testing** - Unit tests with 80%+ coverage requirement
- **🔒 Security First** - Vulnerability scanning, dependency checks, and security headers
- **🐳 Container Ready** - Multi-stage Docker builds with optimization
- **📊 Monitoring & Metrics** - Health checks, performance metrics, and observability
- **🚀 Dual CI/CD** - Both Jenkins and GitHub Actions implementations
- **📧 Smart Notifications** - Email alerts and status reporting
- **🎯 Multi-Environment** - Staging and production deployment support

## 🏛️ Architecture

### Application Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                     Flask Application                           │
├─────────────────────────────────────────────────────────────────┤
│  Routes:                                                        │
│  ├── GET  /              → Home page with app info            │
│  ├── GET  /health        → Health check endpoint              │
│  ├── GET  /api/status    → Application status (JSON)          │
│  ├── GET  /api/version   → Version information                │
│  ├── POST /api/echo      → Echo service for testing           │
│  └── GET  /api/metrics   → Application metrics                │
├─────────────────────────────────────────────────────────────────┤
│  Features:                                                      │
│  ├── 🔒 Security Headers & Rate Limiting                      │
│  ├── 📊 Request/Response Logging                              │
│  ├── ⚡ Performance Monitoring                                │
│  ├── 🏥 Health Checks                                         │
│  └── 📈 Metrics Collection                                    │
└─────────────────────────────────────────────────────────────────┘
```

### CI/CD Pipeline Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Developer     │    │   Git Repository│    │   CI/CD System  │
│   Commits       │───▶│   (GitHub)      │───▶│                │
└─────────────────┘    └─────────────────┘    │  ┌─────────────┐│
                                              │  │ Jenkins     ││
┌─────────────────┐    ┌─────────────────┐    │  └─────────────┘│
│   Docker        │◀───│   Build &       │◀───│  ┌─────────────┐│
│   Registry      │    │   Test          │    │  │GitHub Actions││
└─────────────────┘    └─────────────────┘    │  └─────────────┘│
                                              └─────────────────┘
┌─────────────────┐    ┌─────────────────┐              │
│   Production    │◀───│   Staging       │◀─────────────┘
│   Environment   │    │   Environment   │
└─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (Recommended: 3.9)
- **Docker & Docker Compose**
- **Git**
- **Jenkins** (for Jenkins pipeline)
- **GitHub Account** (for GitHub Actions)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/flask-cicd-demo.git
cd flask-cicd-demo
```

### 2. Local Development Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:5000`

### 3. Run Tests

```bash
# Run all tests with coverage
pytest test_app.py --cov=app --cov-report=html

# Run specific test categories
pytest test_app.py::TestHealthEndpoint -v

# Run linting and formatting
black --check .
flake8 .
isort --check-only .
```

### 4. Docker Deployment

```bash
# Build Docker image
docker build -t flask-cicd-demo:latest .

# Run container
docker run -p 5000:5000 flask-cicd-demo:latest

# Using Docker Compose
docker-compose up -d
```

## 🔧 Jenkins Pipeline Setup

### Prerequisites

1. **Jenkins Installation** with required plugins:
   - Pipeline
   - Docker Pipeline
   - Blue Ocean (recommended)
   - Email Extension
   - Workspace Cleanup

2. **System Configuration**:
   ```bash
   # Add jenkins user to docker group
   sudo usermod -aG docker jenkins
   
   # Install Python and pip
   sudo apt-get install python3 python3-pip python3-venv
   
   # Restart Jenkins
   sudo systemctl restart jenkins
   ```

### Jenkins Credentials Setup

Configure the following credentials in Jenkins:

| Credential ID | Type | Description |
|---------------|------|-------------|
| `dockerhub-credentials` | Username/Password | Docker Hub registry access |
| `github-token` | Secret Text | GitHub personal access token |
| `smtp-credentials` | Username/Password | Email notifications |

### Pipeline Configuration

1. **Create New Pipeline Job**:
   - Go to Jenkins Dashboard → New Item
   - Choose "Pipeline" and enter job name
   - Select "Pipeline script from SCM"
   - Configure Git repository URL

2. **Environment Variables** (Configure in Jenkins):
   ```groovy
   DOCKER_REGISTRY = 'docker.io'
   DOCKER_REPO = 'your-dockerhub-username/flask-cicd-demo'
   EMAIL_RECIPIENTS = 'your-email@company.com'
   STAGING_HOST = 'staging.yourdomain.com'
   PRODUCTION_HOST = 'production.yourdomain.com'
   ```

3. **Email Configuration**:
   - Go to Manage Jenkins → Configure System
   - Configure SMTP server settings
   - Test email configuration

### Jenkins Pipeline Features

- ✅ **Multi-stage builds** with error handling
- ✅ **Parallel code quality checks**
- ✅ **Comprehensive testing** with coverage reports
- ✅ **Security vulnerability scanning**
- ✅ **Docker build and push**
- ✅ **Automated staging deployment**
- ✅ **Production deployment** with approval gates
- ✅ **Performance testing** (optional)
- ✅ **Email notifications**
- ✅ **Artifact management**

### Triggering the Pipeline

```bash
# Automatic trigger on push to main branch
git push origin main

# Manual trigger with parameters
# Use Jenkins UI to trigger with custom parameters
```

## ⚡ GitHub Actions Pipeline Setup

### Repository Secrets Configuration

Configure the following secrets in GitHub repository settings:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `DOCKER_USERNAME` | Docker Hub username | `your-dockerhub-username` |
| `DOCKER_TOKEN` | Docker Hub access token | `dckr_pat_...` |
| `EMAIL_USERNAME` | SMTP email username | `notifications@company.com` |
| `EMAIL_PASSWORD` | SMTP email password | `app-password` |
| `NOTIFICATION_EMAIL` | Email for notifications | `team@company.com` |
| `PRODUCTION_APPROVERS` | Production approvers | `admin,lead-dev` |

### Branch Configuration

The pipeline supports multiple branches:

- **`main`** - Deploys to staging automatically
- **`staging`** - Deploys to staging environment
- **`develop`** - Runs tests only
- **Tags `v*`** - Deploys to production (with approval)

### Workflow Features

- ✅ **Multi-Python version testing** (3.8, 3.9, 3.10, 3.11)
- ✅ **Parallel job execution**
- ✅ **Advanced security scanning** (CodeQL, OWASP)
- ✅ **Multi-platform Docker builds** (AMD64, ARM64)
- ✅ **Blue-green deployment simulation**
- ✅ **Performance testing** with Locust
- ✅ **Manual approval gates** for production
- ✅ **Comprehensive notifications**
- ✅ **Artifact retention management**

### Manual Workflow Triggers

```yaml
# Trigger workflow manually with parameters
workflow_dispatch:
  inputs:
    environment:
      description: 'Deployment environment'
      required: true
      default: 'staging'
      type: choice
      options: ['staging', 'production', 'skip']
```

## 📊 Monitoring & Observability

### Health Checks

The application provides multiple health check endpoints:

```bash
# Basic health check
curl http://localhost:5000/health

# Detailed application status
curl http://localhost:5000/api/status

# Version information
curl http://localhost:5000/api/version

# System metrics
curl http://localhost:5000/api/metrics
```

### Logging

The application uses structured logging:

```python
# Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
# Format: timestamp - logger - level - message
2024-01-15 10:30:45 - app - INFO - Request: GET / - IP: 192.168.1.1
2024-01-15 10:30:45 - app - INFO - Response: 200 - Duration: 0.045s
```

### Metrics Collection

Available metrics:
- Request/response times
- Status code distribution
- Memory and CPU usage
- Active connections
- Error rates

## 🔒 Security Measures

### Application Security

1. **Input Validation & Sanitization**
2. **Rate Limiting** - Prevents abuse
3. **Security Headers** - CORS, CSP, etc.
4. **Non-root Docker containers**
5. **Secret management** - Environment variables
6. **Dependency vulnerability scanning**

### CI/CD Security

1. **Secret scanning** in repositories
2. **Container vulnerability scanning** (Trivy)
3. **Dependency checks** (Safety, OWASP)
4. **Static code analysis** (Bandit)
5. **Multi-factor authentication** for deployments
6. **Audit logging** for all pipeline activities

## 🚀 Deployment Strategies

### Staging Environment

- **Automatic deployment** on main branch changes
- **Feature branch testing**
- **Integration testing**
- **Performance validation**

### Production Environment

- **Manual approval required**
- **Blue-green deployment**
- **Health check validation**
- **Rollback capabilities**
- **Monitoring alerts**

### Environment Configuration

```yaml
# Staging
environment:
  name: staging
  url: https://staging.yourdomain.com

# Production  
environment:
  name: production
  url: https://production.yourdomain.com
```

## 📈 Performance & Scaling

### Load Testing

The project includes comprehensive load testing with Locust:

```python
# Example load test scenarios
- Home page load: 3 requests/second
- Health checks: 2 requests/second  
- API endpoints: 1 request/second
- Echo service: 1 request/second
```

### Performance Benchmarks

- **Response Time**: < 100ms for most endpoints
- **Throughput**: 1000+ requests/second
- **Memory Usage**: < 256MB per container
- **CPU Usage**: < 50% under normal load

### Scaling Configuration

```yaml
# Docker Compose scaling
docker-compose up --scale flask-app=3

# Kubernetes scaling
kubectl scale deployment flask-app --replicas=5
```

## 🔄 CI/CD Pipeline Comparison

| Feature | Jenkins | GitHub Actions |
|---------|---------|----------------|
| **Hosting** | Self-hosted | Cloud-hosted |
| **Configuration** | Groovy (Jenkinsfile) | YAML (.github/workflows) |
| **Plugins** | Extensive ecosystem | Marketplace actions |
| **Build Agents** | Configurable | GitHub-hosted/Self-hosted |
| **Parallel Jobs** | Supported | Native support |
| **Secrets Management** | Jenkins credentials | GitHub secrets |
| **Cost** | Infrastructure costs | Free tier + usage |
| **Integration** | Universal | GitHub-native |

### When to Use Which?

**Choose Jenkins when:**
- Self-hosted infrastructure preferred
- Complex, custom build requirements
- Multiple SCM systems
- Advanced plugin requirements

**Choose GitHub Actions when:**
- GitHub-hosted repositories
- Cloud-native approach preferred
- Integrated GitHub ecosystem
- Faster setup and maintenance

## 📧 Notification Configuration

### Email Notifications

Both pipelines support comprehensive email notifications:

**Jenkins Email Configuration:**
```groovy
emailext (
    subject: "✅ Build SUCCESS: ${JOB_NAME} - Build #${BUILD_NUMBER}",
    body: """
    <h2>🎉 Build Successful!</h2>
    <h3>Build Information:</h3>
    <ul>
        <li>Job: ${JOB_NAME}</li>
        <li>Build Number: ${BUILD_NUMBER}</li>
        <li>Duration: ${currentBuild.durationString}</li>
    </ul>
    """,
    to: "team@company.com",
    mimeType: 'text/html'
)
```

**GitHub Actions Email:**
```yaml
- name: Send Notification Email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 587
    subject: "✅ Flask CI/CD Pipeline - SUCCESS"
    body: |
      ## 🚀 Pipeline Report
      **Status:** ✅ SUCCESS
      **Branch:** ${{ github.ref_name }}
      **Commit:** ${{ github.sha }}
```

### Slack Integration (Optional)

```yaml
# GitHub Actions Slack notification
- name: Slack Notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    channel: '#devops-alerts'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Docker Permission Denied
```bash
# Solution: Add jenkins user to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

#### 2. Python Dependencies Conflict
```bash
# Solution: Use fresh virtual environment
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Test Coverage Below Threshold
```bash
# Check coverage report
coverage report --show-missing
# Add tests for uncovered code
pytest --cov=app --cov-report=html
```

#### 4. Docker Build Failures
```bash
# Check Docker daemon status
sudo systemctl status docker
# Clean Docker cache
docker system prune -f
```

#### 5. GitHub Actions Workflow Failures
- Check repository secrets configuration
- Verify YAML syntax
- Review job dependencies
- Check runner capacity

### Debug Commands

```bash
# Jenkins debugging
tail -f /var/log/jenkins/jenkins.log

# Docker debugging  
docker logs container-name
docker exec -it container-name /bin/bash

# Application debugging
export FLASK_DEBUG=1
export FLASK_ENV=development
python app.py

# GitHub Actions debugging
# Enable debug logging by setting secrets:
# ACTIONS_RUNNER_DEBUG: true
# ACTIONS_STEP_DEBUG: true
```

## 📚 Additional Resources

### Documentation Links
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### Learning Resources
- [CI/CD Best Practices](https://docs.gitlab.com/ee/ci/quick_start/)
- [Python Testing with pytest](https://docs.pytest.org/en/stable/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [Kubernetes Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Development Guidelines

- Follow PEP 8 style guide
- Write comprehensive tests (80%+ coverage)
- Update documentation for new features
- Use conventional commit messages
- Ensure CI/CD pipelines pass

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors & Acknowledgments

- **Your Name** - *Initial work* - [GitHub Profile](https://github.com/your-username)
- **Enterprise DevOps Team** - *CI/CD Pipeline Architecture*

### Special Thanks

- Flask community for the excellent framework
- Jenkins community for robust automation tools
- GitHub for comprehensive DevOps platform
- Docker for containerization technology

---

## 📊 Project Status

- ✅ **Core Application**: Complete
- ✅ **Jenkins Pipeline**: Complete
- ✅ **GitHub Actions**: Complete
- ✅ **Documentation**: Complete
- ✅ **Testing Suite**: Complete (80%+ coverage)
- ✅ **Security Scanning**: Complete
- ✅ **Containerization**: Complete
- ✅ **Monitoring**: Complete

**Last Updated**: January 2024  
**Version**: 1.0.0  
**Status**: Production Ready 🚀