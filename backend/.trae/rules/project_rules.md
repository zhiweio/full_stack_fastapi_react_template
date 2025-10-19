# FastAPI Backend Project Rules

## 🏗️ Architecture & Structure

### Clean Architecture Layers
- **Domain Layer** (`api/domain/`): Business entities, DTOs, interfaces, enums
- **Use Cases** (`api/usecases/`): Application business logic services
- **Interfaces** (`api/interfaces/`): API controllers, middlewares, security
- **Infrastructure** (`api/infrastructure/`): Database, external services, implementations
- **Common** (`api/common/`): Shared utilities, exceptions, base classes

### File Organization
- Follow the established directory structure strictly
- Place new entities in `api/domain/entities/`
- Place DTOs in `api/domain/dtos/`
- Place services in `api/usecases/`
- Place API endpoints in `api/interfaces/api_controllers/`
- Place repository implementations in `api/infrastructure/persistence/repositories/`

## 🔧 Technology Stack & Dependencies

### Core Technologies
- **Framework**: FastAPI with Pydantic v2
- **Database**: PostgreSQL with SQLModel for async operations
- **ORM**: SQLAlchemy 2.0+ with async support
- **Cache**: Redis for sessions and caching
- **Background Tasks**: Celery with Redis broker
- **Authentication**: JWT with PyJWT
- **Dependency Injection**: FastAPI native dependencies

### Required Imports Pattern
```python
from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.core.dependencies import ServiceDep  # Use typed dependencies
from api.domain.dtos.entity_dto import EntityDto
from api.domain.enum.permission import Permission
from api.interfaces.security.role_checker import check_permissions_for_current_role
```

## 📝 Code Style & Conventions

### Naming Conventions
- **Files**: snake_case (e.g., `user_service.py`, `role_endpoint.py`)
- **Classes**: PascalCase (e.g., `UserService`, `RoleRepository`)
- **Functions/Variables**: snake_case (e.g., `get_user_by_id`, `user_data`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `JWT_SECRET`, `DATABASE_URL`)
- **DTOs**: End with `Dto` (e.g., `UserDto`, `CreateUserDto`)
- **Enums**: PascalCase with descriptive names (e.g., `Permission`, `RoleType`)

### Type Annotations
- Always use type hints for function parameters and return types
- Use `Annotated` for dependency injection
- Use Pydantic models for data validation
- Use `Optional` or `| None` for nullable types

### Error Handling
- Use custom exceptions from `api.common.exceptions` and `api.core.exceptions`
- Raise specific exceptions (e.g., `UserNotFoundException`, `EmailAlreadyExistsException`)
- Log errors appropriately using the logger from `api.common.utils.get_logger`

## 🔐 Security & Authentication

### Permission System
- Use `check_permissions_for_current_role()` for endpoint protection
- Define permissions in `api.domain.enum.permission.Permission`
- Support `allow_self_access=True` for user-specific operations
- Always validate user permissions before data access

### JWT & Authentication
- Use `CurrentUser` dependency for authenticated endpoints
- Configure JWT settings in `api.core.config.Settings`
- Handle both access and refresh tokens
- Use environment variables for secrets

## 🗄️ Database & Repository Pattern

### Repository Pattern
- Implement repositories in `api/infrastructure/persistence/repositories/`
- Extend `BaseRepository` for common CRUD operations
- Use async/await for all database operations
- Define repository interfaces in `api/domain/interfaces/`

### Database Sessions
- Use `get_db_session` dependency for database access
- Always use async sessions (`AsyncSession`)
- Handle transactions properly with try/catch blocks

### Migrations
- Use Alembic for database migrations
- Store migrations in `alembic/versions/`
- Configure database URL from environment variables in `alembic/env.py`

## 🔄 Dependency Injection

### FastAPI Dependencies
- Define all dependencies in `api/core/dependencies.py`
- Use typed dependency aliases (e.g., `UserServiceDep`, `RoleRepositoryDep`)
- Follow the pattern: `ServiceDep = Annotated[Service, Depends(get_service)]`
- Inject dependencies at the function parameter level

### Service Layer
- Services should be stateless and focused on business logic
- Inject repositories through constructor dependency injection
- Use dependency functions (not Punq container)
- Initialize services with proper logging

## 📡 API Endpoints

### Router Configuration
- Use `APIRouter` with appropriate prefix and tags
- Group related endpoints in the same router file
- Use proper HTTP status codes (200, 201, 202, 404, etc.)
- Define response models using DTOs

### Endpoint Structure
```python
@router.post("/", response_model=ResponseDto, status_code=status.HTTP_201_CREATED)
async def create_entity(
    data: CreateEntityDto,
    service: EntityServiceDep,
    _: bool = Depends(check_permissions_for_current_role([Permission.ENTITY_CREATE])),
):
    return await service.create_entity(data)
```

## 🧪 Testing

### Test Structure
- Place tests in `tests/` directory
- Use pytest with async support
- Test endpoints in `tests/interfaces/`
- Use descriptive test names and proper assertions

### Test Configuration
- Configure test database separately
- Use fixtures for common test data
- Mock external dependencies when appropriate

## 🌍 Environment & Configuration

### Environment Variables
- Use `.env` file for local development
- Define all settings in `api.core.config.Settings`
- Use Pydantic settings with proper defaults
- Load environment variables with `python-dotenv`

### Multi-Tenancy
- Support header-based and subdomain-based tenancy
- Configure strategy via `MULTI_TENANCY_STRATEGY` environment variable
- Implement tenant isolation at the database level

## 📦 Package Management

### Dependencies
- Use `uv` for package management
- Define dependencies in `pyproject.toml`
- Pin major versions for stability
- Separate development and production dependencies

## 🚀 Development Workflow

### Code Quality
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Write docstrings for complex functions
- Keep functions focused and single-purpose

### Logging
- Use structured logging with `colorlog`
- Import logger: `from api.common.utils import get_logger`
- Log important operations and errors
- Use appropriate log levels (INFO, WARNING, ERROR)

### Performance
- Use async/await for I/O operations
- Implement proper caching strategies with Redis
- Use background tasks for heavy operations
- Optimize database queries and use proper indexing

## 🔒 Security Best Practices

- Never commit secrets or API keys
- Use environment variables for sensitive configuration
- Validate all input data using Pydantic models
- Implement proper CORS configuration
- Use HTTPS in production environments
- Sanitize user inputs to prevent injection attacks

## 📚 Documentation

- Update API documentation when adding new endpoints
- Use clear and descriptive docstrings
- Document complex business logic
- Keep README.md updated with architecture changes