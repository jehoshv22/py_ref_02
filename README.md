# User REST API

A simple Flask REST API for managing users with GET and POST endpoints.

## Features

- **GET /api/users** - Retrieve all users
- **GET /api/users/<id>** - Retrieve a specific user by ID
- **POST /api/users** - Create a new user
- **DELETE /api/users/<id>** - Delete a user by ID
- **GET /api/health** - Health check endpoint

## Project Structure

```
py_ref_02/
├── app/
│   ├── __init__.py
│   ├── api.py              # Flask API routes
│   └── models.py           # User and UserStore models
├── tests/
│   ├── conftest.py         # Pytest configuration
│   └── test_api.py         # Unit tests
├── run.py                  # Application entry point
├── requirements.txt        # Project dependencies
└── README.md              # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

For **production/runtime only**:
```bash
pip install -r requirements.txt
```

For **development (includes testing and linting tools)**:
```bash
pip install -r requirements-dev.txt
```

## Running the Application

```bash
python run.py
```

The API server will start at [http://localhost:5000](http://localhost:5000)

## Running with Docker

### Build Docker Image
```bash
docker build -t user-api:latest .
```

### Run Docker Container
```bash
docker run -p 5000:5000 user-api:latest
```

### Docker Compose (Optional)
For more advanced deployments, create a `docker-compose.yml` file:
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
```

Then run:
```bash
docker-compose up
```

## API Endpoints

### GET All Users
```bash
curl http://localhost:5000/api/users
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
]
```

### GET User by ID
```bash
curl http://localhost:5000/api/users/1
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

### POST Create User
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

### DELETE User
```bash
curl -X DELETE http://localhost:5000/api/users/1
```

**Response:**
```json
{
  "message": "User deleted successfully"
}
```

### Health Check
```bash
curl http://localhost:5000/api/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

## Running Tests

Run all tests with pytest:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=app tests/
```

Run tests with verbose output:
```bash
pytest -v
```

## Code Quality & Linting

The project includes tools for code formatting and linting:

### Flake8 - Style Guide Enforcement
Check code for style violations:
```bash
flake8 app tests
```

### Black - Code Formatter
Automatically format code to match style standards:
```bash
black app tests
```

### isort - Import Sorting
Automatically sort imports:
```bash
isort app tests
```

Configuration files:
- `.flake8` - Flake8 configuration
- `pyproject.toml` - Black and isort configuration

## Continuous Integration

This project uses **GitHub Actions** to automatically run linting, unit tests, and Docker builds on every push and pull request.

### Workflow
The workflow defined in [.github/workflows/ci.yml](.github/workflows/ci.yml) includes two jobs:

**1. Lint and Test Job**
- Runs on: Python 3.10, 3.11, and 3.12
- **Linting**: Validates code style with flake8
- **Testing**: Executes all unit tests with pytest
- **Coverage**: Generates both XML and HTML coverage reports
- **Artifacts**: Exports coverage reports (XML and HTML) to pipeline artifacts (30-day retention)
- **Codecov**: Uploads coverage reports to Codecov

**2. Docker Build Job** (Runs on push to main/develop after tests pass)
- **Build**: Builds Docker image using multi-stage build
- **Cache**: Leverages GitHub Actions cache for faster builds
- **Artifacts**: Exports Docker image tar file to pipeline artifacts (7-day retention)

### Status Badge
[![CI/CD Pipeline](https://github.com/<username>/<repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<username>/<repo>/actions/workflows/ci.yml)

*Note: Update the username and repo in the badge URL*

## Test Coverage

The test suite includes:
- **User Model Tests** - Tests for User and UserStore classes
- **API Endpoint Tests** - All CRUD operations
- **Error Handling Tests** - Invalid inputs and edge cases
- **Total Tests** - 20+ test cases

## API Error Responses

### 400 Bad Request
```json
{
  "error": "Missing required fields: name, email"
}
```

### 404 Not Found
```json
{
  "error": "User not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Notes

- This is a simple in-memory storage implementation. Data will be lost when the server restarts.
- User IDs are auto-incremented starting from 1.
- Email validation is not implemented in this basic version.

## License

MIT
