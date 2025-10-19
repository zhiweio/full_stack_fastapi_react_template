# FastAPI Backend API

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

A production-ready FastAPI backend API built with Clean Architecture principles, featuring multi-tenancy, comprehensive user management, AI integration, and cloud storage support. Uses PostgreSQL with SQLModel for robust data persistence.

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Pull and run the container
docker run -d \
  --name fastapi-backend \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://postgres:password@your-db-host:5432/your_database \
  -e JWT_SECRET=your-secret-key \
  your-registry/fastapi-backend:latest

# Access the API
curl http://localhost:8000/health
```

### Environment Variables

```bash
# Required Environment Variables
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/your_database
JWT_SECRET=your-jwt-secret-key
REFRESH_TOKEN_SECRET=your-refresh-secret-key

# Optional Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=SecurePassword123!
```

## ✨ Key Features

### 🔐 Authentication & Authorization
- **JWT Authentication** with access and refresh tokens
- **Role-Based Access Control (RBAC)** with granular permissions
- **Multi-factor Authentication** support
- **Password Reset** with email verification
- **Session Management** with automatic token refresh

### 🏢 Multi-Tenant Architecture
- **Flexible Multi-Tenancy** with header or subdomain strategies
- **Tenant Isolation** with secure data separation
- **Dynamic Tenant Creation** with automated setup
- **Subdomain Management** with availability checking
- **Tenant-Scoped Permissions** and role assignments

### 👥 User Management
- **Complete User CRUD** operations with validation
- **User Profile Management** with image upload support
- **Account Activation/Deactivation** workflows
- **Role Assignment** within tenant contexts
- **User Search and Filtering** capabilities

### 🎭 Role & Permission System
- **Dynamic Role Creation** with custom permissions
- **Permission Matrix** for fine-grained access control
- **Role Inheritance** and hierarchical permissions
- **Runtime Permission Checking** with decorators


### 🤖 AI Integration
- **Local AI Models** integration with Ollama support
- **Real-time Streaming** responses for chat interfaces
- **Conversation History** with persistent storage
- **Multiple Model Support** with dynamic switching


### ☁️ Cloud Storage
- **Azure Blob Storage** native integration
- **AWS S3 Compatible** storage support
- **File Upload Management** with validation and processing
- **Storage Provider Abstraction** for easy switching
- **Secure File Access** with signed URLs

### 📧 Email System
- **Async Email Sending** with FastAPI-Mail
- **Template Engine** for dynamic email content
- **Background Processing** with Celery integration
- **SMTP Configuration** with multiple provider support
- **Email Verification** workflows

### ⚡ Background Processing
- **Celery Integration** with Redis broker
- **Async Task Processing** for heavy operations
- **Task Monitoring** with Flower dashboard
- **Retry Logic** and error handling
- **Scheduled Tasks** support

## 🏗️ Architecture

### Clean Architecture Layers

```
api/
├── domain/              # Business Logic Layer
│   ├── entities/       # Core business entities
│   ├── dtos/           # Data transfer objects
│   ├── interfaces/     # Abstract interfaces
│   └── enum/           # Domain enums and constants
├── usecases/           # Application Business Rules
│   ├── auth_service.py
│   ├── user_service.py
│   ├── tenant_service.py
│   ├── role_service.py
│   └── local_ai_service.py
├── interfaces/         # Interface Adapters
│   ├── api_controllers/ # REST API endpoints
│   ├── middlewares/    # HTTP middlewares
│   └── security/       # Authentication handlers
├── infrastructure/     # Frameworks & Drivers
│   ├── persistence/    # Database implementations
│   ├── externals/      # Third-party integrations
│   ├── messaging/      # Message brokers
│   └── cache/          # Caching implementations
└── common/             # Shared Utilities
    ├── exceptions/     # Custom exceptions
    ├── utils/          # Helper functions
    └── dtos/           # Common DTOs
```

### Technology Stack

- **Framework**: FastAPI 0.116+ with Pydantic v2
- **Database**: PostgreSQL with SQLModel for async operations
- **Cache**: Redis for session storage and caching
- **Background Tasks**: Celery with Redis broker
- **Authentication**: JWT with PyJWT
- **AI**: LangChain with Ollama integration
- **Storage**: Azure Blob Storage, AWS S3 compatible
- **Email**: FastAPI-Mail with async SMTP
- **Security**: Passlib for password hashing
- **Dependency Injection**: FastAPI dependencies
- **Testing**: Pytest with async support


## ⚙️ Configuration

### Environment Variables
```bash
  # PostgreSQL settings
  DATABASE_URL=postgresql+asyncpg://postgres:password@127.0.0.1:5432/postgres

  # JWT settings
  JWT_SECRET=your_jwt_secret_key
  REFRESH_TOKEN_SECRET=your_refresh_jwt_secret_key

  # Configure your default app admin credentials.
  ADMIN_EMAIL=admin@example.com
  ADMIN_PASSWORD=Test@123!

  # SMTP Email settings
  SMTP_HOST="localhost"
  SMTP_PORT=1023
  SMTP_USER=""
  SMTP_PASSWORD=""
  SMTP_MAIL_FROM="noreply@example.com"
  SMTP_MAIL_FROM_NAME="Full-Stack Fast API"
  SMTP_STARTTLS=False
  SMTP_SSL_TLS=False

  # Redis settings

  REDIS_URI="redis://localhost:6372/0"

  # App configuration
  APP_TITLE="Full-Stack FastAPI React Template"
  APP_VERSION="0.1.0"

  API_ENDPOINT_BASE="http://localhost:8000/api"

  # Configure Multi-Tenancy
  MULTI_TENANCY_STRATEGY="header"  # Options: "header", "subdomain", "none"

  # Host main domain name
  HOST_MAIN_DOMAIN="fsrapp.com"

  # Ollama settings
  OLLAMA_HOST="http://localhost:11434"
```


## 🚀 Development

### Local Development

```bash
# Install dependencies
uv sync

# Start development server
uv run fastapi dev

# Run with auto-reload
uv run fastapi dev --reload

# Run background worker
uv run celery -A api.infrastructure.messaging.celery_worker worker --loglevel=info

# Monitor tasks with Flower
uv run celery -A api.infrastructure.messaging.celery_worker flower
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=api

# Run specific test file
uv run pytest tests/interfaces/test_user_endpoint.py
```

## 📊 Monitoring & Observability

### Health Checks

```bash
# API Health
GET /health


### Logging

- **Structured Logging** with colorlog
- **Request/Response Logging** with correlation IDs
- **Error Tracking** with detailed stack traces
- **Performance Metrics** for API endpoints

### Background Task Monitoring

```bash
# Flower Dashboard
http://localhost:5555

# Celery Status
celery -A api.infrastructure.messaging.celery_worker status
```

## 🤝 Contributing

1. **Clean Architecture**: Follow the established layer separation
2. **Type Safety**: Use Pydantic models for all data validation
3. **Testing**: Add tests for new features and endpoints
4. **Documentation**: Update API documentation for changes
5. **Security**: Follow security best practices for new code

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Production Ready**: This API is designed for production use with comprehensive security, scalability, and monitoring features built-in.