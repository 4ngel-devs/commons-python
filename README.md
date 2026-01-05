# Commons Python

A shared Python library containing common utilities, data models, and response structures for Phoenix projects.

## Features

- **Custom Exceptions**: Exception classes for error handling (`BusinessException` as main exception)
- **API Response DTO**: Standardized API response structure with pagination support
- **Pagination**: Pagination data model with sorting support for paginated responses
- **BaseAuditDto**: Base DTO with audit fields (created_by, created_at, updated_by, updated_at)
- **Sort Utils**: Utilities for parsing and creating sort objects
- **Pagination Utils**: Utilities for working with pagination objects
- **Keycloak Integration**: Keycloak authentication provider with automatic reconnection
- **Keycloak User Model**: Model for representing authenticated Keycloak users
- **Keycloak JWT Decoder**: Decode JWT tokens to extract user information
- **Date Utils**: Date and datetime utilities with Mexico timezone support
- **Logging**: Integrated with Loguru for structured logging

## Requirements

- Python >= 3.11
- [uv](https://github.com/astral-sh/uv) package manager

## Setup

### 1. Install Python 3.11 using uv

```bash
uv python install 3.11
uv python pin 3.11
```

### 2. Initialize and Create Virtual Environment

```bash
uv venv --python 3.11
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install main dependencies
uv sync

# Install with development dependencies (includes pytest)
uv sync --extra dev
```

## Project Structure

```
commons-python/
├── sucrim/
│   ├── dto/                       # Data Transfer Objects
│   │   ├── __init__.py
│   │   └── base_audit_dto.py      # Base DTO with audit fields
│   ├── http/                      # HTTP utilities
│   │   ├── __init__.py
│   │   ├── exception_handlers.py  # FastAPI exception handlers
│   │   ├── errors/                # HTTP error/exception classes
│   │   │   ├── __init__.py
│   │   │   ├── business_exception.py  # Main exception for business logic
│   │   │   ├── bad_request_exception.py  # HTTP 400 exception
│   │   │   ├── unauthorized_exception.py  # HTTP 401 exception
│   │   │   ├── forbidden_exception.py  # HTTP 403 exception
│   │   │   ├── not_found_exception.py  # HTTP 404 exception
│   │   │   ├── conflict_exception.py  # HTTP 409 exception
│   │   │   ├── unprocessable_entity_exception.py  # HTTP 422 exception
│   │   │   ├── internal_server_error_exception.py  # HTTP 500 exception
│   │   │   ├── service_unavailable_exception.py  # HTTP 503 exception
│   │   │   └── validation_exception.py  # Validation exception
│   │   └── response/               # HTTP response structures
│   │       ├── __init__.py
│   │       └── api_response_dto.py    # API response DTO
│   ├── keycloak/                  # Keycloak authentication modules
│   │   ├── __init__.py
│   │   ├── keycloak_config.py    # Keycloak configuration
│   │   ├── keycloak_auth_provider.py  # Keycloak auth provider with auto-reconnect
│   │   ├── keycloak_jwt_decoder.py  # JWT token decoder for user information
│   │   └── keycloak_user.py      # Keycloak user model
│   ├── models/                    # Data models
│   │   ├── __init__.py
│   │   ├── pagination.py          # Pagination model with sorting
│   │   └── sort_info.py           # Sort information model
│   └── utils/                     # Utility modules
│       ├── __init__.py
│       ├── date_utils.py          # Date utilities with Mexico timezone
│       ├── pagination_utils.py    # Pagination utilities
│       └── sort_utils.py          # Sort utilities
├── tests/
│   ├── __init__.py
│   └── test_date_utils.py         # Test suite
├── pyproject.toml                 # Project configuration
└── README.md
```

## Usage

### Custom Exceptions

**BusinessException** is the main exception class for business logic errors. Use it for domain-specific errors and business rule violations.

```python
# Option 1: Import from http (re-exported for convenience)
from sucrim.http import BusinessException, ValidationException, NotFoundException

# Option 2: Import directly from errors (more explicit)
from sucrim.http.errors import BusinessException, ValidationException, NotFoundException

# Main exception for business logic errors
raise BusinessException(
    message="Insufficient balance",
    process="process_payment",
    status_code=400
)

# Validation errors
raise ValidationException(
    message="Invalid email format",
    process="validate_user",
    errors=[{"field": "email", "message": "Must be a valid email"}]
)

# Not found errors
raise NotFoundException(
    message="User not found",
    process="get_user"
)
```

**Available exceptions:**
- `BusinessException` - Main exception for business logic errors (default status: 400)
- `ValidationException` - Input validation errors (default status: 422)
- `BadRequestException` - Bad request errors (status: 400)
- `UnauthorizedException` - Authentication errors (status: 401)
- `ForbiddenException` - Authorization errors (status: 403)
- `NotFoundException` - Resource not found (status: 404)
- `ConflictException` - Resource conflicts (status: 409)
- `UnprocessableEntityException` - Unprocessable entity (status: 422)
- `InternalServerErrorException` - Server errors (status: 500)
- `ServiceUnavailableException` - Service unavailable (status: 503)

### API Response DTO

```python
from sucrim.http.response import ApiResponseDto
from sucrim.models import Pagination

# Simple response
response = ApiResponseDto.ok({"message": "Success"})

# Paginated response with sorting
pagination = Pagination(page=1, page_size=10, sort_by="name", sort_direction="asc")
response = ApiResponseDto.ok_with_pagination([1, 2, 3], pagination)

# Paginated response with total elements
response = ApiResponseDto.ok_from_page(
    [1, 2, 3], 
    pagination, 
    total_elements=100
)
```

### Pagination with Sorting

```python
from sucrim.models import Pagination

# Create pagination with sorting
pagination = Pagination(
    page=1,
    page_size=20,
    sort_by="created_at",
    sort_direction="desc"
)

# Set total elements (automatically calculates total_pages)
pagination.set_total_elements(150)
```

### Sort Utils

```python
from sucrim.utils import SortUtils
from sucrim.models import SortInfo

# Parse sort string
sort_infos = SortUtils.parse_sort("name:asc,createdAt:desc")
# Returns: [SortInfo(field='name', direction='asc'), SortInfo(field='createdAt', direction='desc')]

# Create sort from field and direction
sort_infos = SortUtils.create_sort("name", "desc")
# Returns: [SortInfo(field='name', direction='desc')]

# Convert to dictionary format (useful for ORM queries)
sort_dicts = SortUtils.to_sort_dict(sort_infos)
# Returns: [{'field': 'name', 'direction': 'desc'}]
```

### Pagination Utils

```python
from sucrim.utils import PaginationUtils
from sucrim.models import Pagination

pagination = Pagination(page=1, page_size=10, sort_by="name", sort_direction="asc")

# Get pageable parameters (0-indexed page, size)
page_index, page_size = PaginationUtils.create_pageable_params(pagination)
# Returns: (0, 10)

# Get pageable with sort information
page_index, page_size, sort_infos = PaginationUtils.create_pageable_with_sort(pagination)
# Returns: (0, 10, [SortInfo(field='name', direction='asc')])

# Get as dictionary (useful for ORM queries)
pageable_dict = PaginationUtils.create_pageable_dict(pagination)
# Returns: {'page': 0, 'size': 10, 'sort': [{'field': 'name', 'direction': 'asc'}]}
```

### BaseAuditDto

```python
from sucrim.dto import BaseAuditDto
from datetime import datetime

# Extend BaseAuditDto for DTOs that need audit fields
class UserDto(BaseAuditDto):
    username: str
    email: str

# Create DTO with audit fields
user = UserDto(
    username="john_doe",
    email="john@example.com",
    created_by="admin",
    created_at=datetime.now(),
    updated_by="admin",
    updated_at=datetime.now()
)
```

### Keycloak Authentication

```python
from sucrim.keycloak import KeycloakAuthProvider, KeycloakUser, KeycloakConfig, KeycloakJwtDecoder

# Initialize auth provider
config = KeycloakConfig()  # Reads from environment variables
auth_provider = KeycloakAuthProvider(config)

# Get admin access token
token = auth_provider.get_admin_access_token()
bearer_token = auth_provider.get_admin_access_token_string()  # Includes "Bearer " prefix

# Get HTTP client for making authenticated requests
client = await auth_provider.get_client()
response = await client.get("https://api.example.com/resource", headers={
    "Authorization": bearer_token
})

# Close client when done
await auth_provider.close()
```

### Keycloak User Model

```python
from sucrim.keycloak import KeycloakUser

# Create Keycloak user from token or API response
user = KeycloakUser(
    username="john_doe",
    keycloak_user_id="123e4567-e89b-12d3-a456-426614174000",
    tenant_id="tenant-123",
    email="john@example.com",
    first_name="John",
    last_name="Doe",
    realm="my-realm",
    client_id="my-client",
    roles=["user", "admin"],
    email_verified=True
)
```

### Keycloak JWT Decoder

The `KeycloakJwtDecoder` decodes JWT tokens from Keycloak and extracts user information. It automatically logs warnings when claims are missing from the token.

#### Basic Usage

```python
from sucrim.keycloak import KeycloakJwtDecoder
from sucrim.http.errors import UnauthorizedException

# Decode JWT token and extract user information
token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."  # Token from request header

try:
    user = KeycloakJwtDecoder.decode_token(token)
    
    # Access user information
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Tenant ID: {user.tenant_id}")
    print(f"Roles: {user.roles}")
    print(f"Realm: {user.realm}")
    
except UnauthorizedException as e:
    print(f"Failed to decode token: {e.message}")
```

#### Usage in FastAPI with Dependencies

```python
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sucrim.keycloak import KeycloakJwtDecoder, KeycloakUser
from sucrim.http.errors import UnauthorizedException

app = FastAPI()
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> KeycloakUser:
    """
    Dependency to get current authenticated user from JWT token.
    
    Usage:
        @app.get("/protected")
        async def protected_route(user: KeycloakUser = Depends(get_current_user)):
            return {"message": f"Hello {user.username}"}
    """
    try:
        token = credentials.credentials
        user = KeycloakJwtDecoder.decode_token(token)
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
            
        return user
    except UnauthorizedException as e:
        raise HTTPException(status_code=401, detail=e.message)

@app.get("/users/me")
async def get_current_user_info(user: KeycloakUser = Depends(get_current_user)):
    """Get current authenticated user information."""
    return {
        "username": user.username,
        "email": user.email,
        "tenant_id": user.tenant_id,
        "roles": user.roles,
        "realm": user.realm
    }
```

#### Usage with Role-Based Access Control

```python
from fastapi import Depends, HTTPException
from sucrim.keycloak import KeycloakJwtDecoder, KeycloakUser
from sucrim.http.errors import UnauthorizedException, ForbiddenException

def require_role(required_role: str):
    """
    Dependency factory to require a specific role.
    
    Usage:
        @app.get("/admin")
        async def admin_route(user: KeycloakUser = Depends(require_role("admin"))):
            return {"message": "Admin access granted"}
    """
    def role_checker(user: KeycloakUser = Depends(get_current_user)) -> KeycloakUser:
        if required_role not in user.roles:
            raise ForbiddenException(
                message=f"User does not have required role: {required_role}",
                process="role_validation"
            )
        return user
    return role_checker

@app.get("/admin/users")
async def list_users(user: KeycloakUser = Depends(require_role("admin"))):
    """Admin-only endpoint to list users."""
    return {"message": f"Listing users for admin: {user.username}"}
```

#### Usage with Tenant Validation

```python
from sucrim.keycloak import KeycloakJwtDecoder, KeycloakUser
from sucrim.http.errors import UnauthorizedException

def get_current_user_with_tenant(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> KeycloakUser:
    """
    Dependency that requires tenant_id in token.
    """
    try:
        token = credentials.credentials
        user = KeycloakJwtDecoder.decode_token(token)
        
        if not user.tenant_id:
            raise UnauthorizedException(
                message="Tenant ID is required but missing in token",
                process="tenant_validation"
            )
            
        return user
    except UnauthorizedException as e:
        raise HTTPException(status_code=401, detail=e.message)

@app.get("/tenant/data")
async def get_tenant_data(user: KeycloakUser = Depends(get_current_user_with_tenant)):
    """Get data for the user's tenant."""
    return {
        "tenant_id": user.tenant_id,
        "data": f"Data for tenant {user.tenant_id}"
    }
```

#### Manual Token Extraction from Headers

```python
from fastapi import Request
from sucrim.keycloak import KeycloakJwtDecoder
from sucrim.http.errors import UnauthorizedException

@app.get("/custom-auth")
async def custom_auth_endpoint(request: Request):
    """Example with manual token extraction."""
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    try:
        # KeycloakJwtDecoder handles "Bearer " prefix automatically
        user = KeycloakJwtDecoder.decode_token(auth_header)
        
        return {
            "user": user.username,
            "email": user.email,
            "roles": user.roles
        }
    except UnauthorizedException as e:
        raise HTTPException(status_code=401, detail=e.message)
```

#### Extracted Claims Mapping

The decoder extracts the following information from JWT tokens:

| KeycloakUser Field | JWT Claim | Description |
|-------------------|-----------|-------------|
| `username` | `preferred_username` | Username of the authenticated user |
| `keycloak_user_id` | `sid` | Keycloak session/user ID |
| `tenant_id` | `tenantId` | Tenant ID for multi-tenant applications |
| `email` | `email` | User email address |
| `first_name` | `given_name` | User first name |
| `last_name` | `family_name` | User last name |
| `realm` | `iss` (extracted) or `realm` | Keycloak realm name |
| `client_id` | `azp` | Authorized party (client ID) |
| `roles` | `realm_access.roles` + `resource_access.*.roles` | Combined list of realm and client roles |
| `email_verified` | `email_verified` | Whether email is verified |

**Note**: The decoder logs warnings when claims are missing from the token, making it easy to debug token issues during development.

**Security Note**: The decoder extracts claims without signature verification. For production, you should verify the signature using Keycloak's public key for security.

### Date Utils

```python
from sucrim.utils import DateUtils

# Get current Mexico time
now = DateUtils.now()  # datetime with Mexico timezone

# Get current Mexico date
today = DateUtils.today()  # date object

# Convert to Mexico timezone
from datetime import datetime
from zoneinfo import ZoneInfo

utc_dt = datetime(2024, 1, 15, 18, 0, 0, tzinfo=ZoneInfo("UTC"))
mexico_dt = DateUtils.to_mexico_timezone(utc_dt)

# Convert from Mexico timezone to UTC
utc_dt = DateUtils.from_mexico_timezone(mexico_dt, ZoneInfo("UTC"))
```

## Testing

**Important**: Make sure you have installed development dependencies first:
```bash
uv sync --extra dev
```

### Run All Tests

```bash
uv run pytest
```

### Run Tests with Verbose Output

```bash
uv run pytest -vv
```

### Run Tests with Coverage Report

```bash
uv run pytest --cov=sucrim --cov-report=term-missing
```

### Run Tests with HTML Coverage Report

```bash
uv run pytest --cov=sucrim --cov-report=html
# Open htmlcov/index.html in your browser
```

### Run Specific Test File

```bash
uv run pytest tests/test_date_utils.py
```

### Run Specific Test Class or Method

```bash
uv run pytest tests/test_date_utils.py::TestDateUtils
uv run pytest tests/test_date_utils.py::TestDateUtils::test_now_returns_datetime_with_mexico_timezone
```

## Adding New Implementations

When adding new features to this shared library, follow these best practices:

### 1. Code Organization

- Place new modules in the appropriate directory under `src/`:
  - `src/data/` - Data models and DTOs
  - `src/response/` - Response structures
  - `src/utils/` - Utility functions and helper classes
  - Create new directories as needed (e.g., `src/exceptions/`, `src/validators/`)

### 2. Package Structure

- Always create `__init__.py` files in each package directory
- Export public classes/functions in `__init__.py` using `__all__`
- Use absolute imports: `from sucrim.module import Class` (not relative imports)

### 3. Type Hints

- Use type hints for all function parameters and return types
- Use `Generic[T]` for generic classes
- Import types from `typing` module when needed

### 4. Documentation

- Add docstrings to all public classes and methods
- Use Google-style or NumPy-style docstrings
- Include examples in docstrings for complex functions

### 5. Testing

- Write tests for all new functionality
- Place tests in `tests/` directory
- Follow naming convention: `test_<module_name>.py`
- Use descriptive test method names: `test_<functionality>_<expected_behavior>`
- Aim for high test coverage (ideally >80%)

### 6. Dependencies

- Add new dependencies to `pyproject.toml` in the `dependencies` section
- Add test-only dependencies to `[project.optional-dependencies].dev`
- Specify minimum versions (e.g., `"package>=1.0.0"`)

### 7. Example: Adding a New Utility

```python
# src/utils/new_util.py
"""New utility module."""

from loguru import logger


class NewUtil:
    """Utility class for new functionality."""

    @staticmethod
    def do_something(param: str) -> str:
        """
        Do something useful.

        Args:
            param: Input parameter

        Returns:
            Result string
        """
        logger.debug(f"Processing: {param}")
        return f"Processed: {param}"
```

```python
# src/utils/__init__.py
"""Utility modules for common operations."""

from .date_utils import DateUtils
from .new_util import NewUtil

__all__ = ["DateUtils", "NewUtil"]
```

```python
# tests/test_new_util.py
"""Tests for NewUtil class."""

import pytest
from sucrim.utils import NewUtil


class TestNewUtil:
    """Test cases for NewUtil."""

    def test_do_something_returns_processed_string(self):
        """Test that do_something processes the input correctly."""
        result = NewUtil.do_something("test")
        assert result == "Processed: test"
```

## Using in Other Python Projects

This shared library can be installed in other Python projects directly from GitHub.

### For Public Repositories

If the repository is public, you can install it directly:

```bash
# Using uv
uv pip install git+https://github.com/your-org/commons-python.git

# Using pip
pip install git+https://github.com/your-org/commons-python.git

# Install specific branch or tag
uv pip install git+https://github.com/your-org/commons-python.git@main
uv pip install git+https://github.com/your-org/commons-python.git@v0.1.0
```

### For Private Repositories

For private repositories, you have several options:

#### Option 1: Using SSH (Recommended)

```bash
# Using uv - install latest from main branch
uv pip install git+ssh://git@github.com/your-org/commons-python.git

# Install from specific tag
uv pip install git+ssh://git@github.com/your-org/commons-python.git@v0.1.0

# Install from specific branch
uv pip install git+ssh://git@github.com/your-org/commons-python.git@main

# Using pip
pip install git+ssh://git@github.com/your-org/commons-python.git
pip install git+ssh://git@github.com/your-org/commons-python.git@v0.1.0
```

**Setup SSH key:**
1. Generate SSH key if you don't have one: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Add SSH key to your GitHub account: Settings → SSH and GPG keys → New SSH key
3. Test connection: `ssh -T git@github.com`

#### Option 2: Using HTTPS with Personal Access Token

```bash
# Using uv - install latest from main branch
uv pip install git+https://<TOKEN>@github.com/your-org/commons-python.git

# Install from specific tag
uv pip install git+https://<TOKEN>@github.com/your-org/commons-python.git@v0.1.0

# Install from specific branch
uv pip install git+https://<TOKEN>@github.com/your-org/commons-python.git@main

# Using pip
pip install git+https://<TOKEN>@github.com/your-org/commons-python.git
pip install git+https://<TOKEN>@github.com/your-org/commons-python.git@v0.1.0
```

**Create Personal Access Token:**
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. Use token in the URL (replace `<TOKEN>`)

#### Option 3: Using Git Credentials

Configure Git to use credentials:

```bash
# Store credentials
git config --global credential.helper store

# Then install
uv pip install git+https://github.com/your-org/commons-python.git
# Enter your GitHub username and Personal Access Token when prompted
```

#### Option 4: Add to requirements.txt or pyproject.toml

**In requirements.txt:**
```
# Install from main branch (latest)
git+ssh://git@github.com/your-org/commons-python.git
# or
git+https://<TOKEN>@github.com/your-org/commons-python.git

# Install from specific tag (recommended for production)
git+ssh://git@github.com/your-org/commons-python.git@v0.1.0
# or
git+https://<TOKEN>@github.com/your-org/commons-python.git@v0.1.0

# Install from specific branch
git+ssh://git@github.com/your-org/commons-python.git@develop
```

**In pyproject.toml:**
```toml
[project]
dependencies = [
    # Install from main branch (latest)
    "commons-python @ git+ssh://git@github.com/your-org/commons-python.git",
    # or
    "commons-python @ git+https://<TOKEN>@github.com/your-org/commons-python.git",
    
    # Install from specific tag (recommended for production)
    "commons-python @ git+ssh://git@github.com/your-org/commons-python.git@v0.1.0",
    # or
    "commons-python @ git+https://<TOKEN>@github.com/your-org/commons-python.git@v0.1.0",
    
    # Install from specific branch
    "commons-python @ git+ssh://git@github.com/your-org/commons-python.git@develop",
]
```

**Note:** When using tags, replace `v0.1.0` with your actual tag name (e.g., `v1.0.0`, `v2.3.1`, etc.). Using tags is recommended for production environments to ensure version stability.

Then install:
```bash
uv pip install -r requirements.txt
# or
uv pip install .
```

### Working with Tags

Tags are recommended for production use as they provide version stability. Here's how to work with them:

**Create a new tag:**
```bash
# Create an annotated tag (recommended)
git tag -a v0.1.0 -m "Release version 0.1.0"

# Push tag to remote
git push origin v0.1.0

# Push all tags
git push origin --tags
```

**List available tags:**
```bash
# List all tags
git tag

# List tags matching a pattern
git tag -l "v0.*"

# Show tag details
git show v0.1.0
```

**Install from a tag:**
```bash
# Using uv
uv pip install git+ssh://git@github.com/your-org/commons-python.git@v0.1.0

# Using pip
pip install git+ssh://git@github.com/your-org/commons-python.git@v0.1.0
```

### Installing in Editable Mode (Development)

If you're actively developing and want changes to reflect immediately:

```bash
# Clone the repository first
git clone git@github.com/your-org/commons-python.git
cd commons-python

# Install in editable mode
uv pip install -e .

# In your project, install from local path
uv pip install -e /path/to/commons-python
```

### Using in Your Project

Once installed, import and use the modules:

```python
from sucrim.http import BusinessException
from sucrim.http.response import ApiResponseDto
from sucrim.models import Pagination
from sucrim.utils import DateUtils, SortUtils, PaginationUtils
from sucrim.dto import BaseAuditDto
from sucrim.keycloak import KeycloakAuthProvider, KeycloakUser, KeycloakJwtDecoder

# Your code here
response = ApiResponseDto.ok({"data": "example"})
now = DateUtils.now()

# Use BusinessException for business logic errors
if balance < amount:
    raise BusinessException(
        message="Insufficient balance",
        process="process_payment"
    )
```

## Development

### Running Tests

**Important**: Make sure you have installed development dependencies first:
```bash
uv sync --extra dev
```

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=sucrim --cov-report=html
```

### Code Quality

This project uses:
- **Pydantic** for data validation
- **Loguru** for logging
- **pytest** for testing
- **pytest-cov** for coverage reporting

## License


## Contributing

