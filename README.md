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

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python run.py
```

The API server will start at [http://localhost:5000](http://localhost:5000)

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
