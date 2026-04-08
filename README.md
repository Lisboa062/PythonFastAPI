# PythonFastAPI

[![CI - Initial Testing](https://github.com/Lisboa062/PythonFastAPI/actions/workflows/ci.yml/badge.svg)](https://github.com/Lisboa062/PythonFastAPI/actions/workflows/ci.yml)

A backend API built with **FastAPI**, following clean architecture principles and featuring JWT authentication, automated testing, and a fully containerized environment with Docker.

---

## About the project

This project is a backend API for user authentication and order management, designed with a strong focus on:

- Clear separation of responsibilities  
- Decoupled business logic  
- Secure authentication using JWT  
- Automated testing  
- Reproducible environment with Docker  
- PostgreSQL database with schema control via Alembic  

---

## Tech Stack

- Python  
- FastAPI  
- SQLAlchemy  
- PostgreSQL  
- Alembic  
- Pytest  
- Docker  
- Docker Compose  
- GitHub Actions  
- JWT (JSON Web Token)  
- Pydantic  

---

## Architecture

The project follows a layered architecture:

```text
app/
├── routers        # HTTP entry layer
├── services       # Business logic
├── repositories   # Data access layer
├── models         # SQLAlchemy models
├── schemas        # Pydantic schemas
├── core           # Config, security, exceptions
└── dependencies   # Auth and DB session
```

---

## Request Flow

```text
Request → Router → Service → Repository → Database
```

---

## Authentication

- JWT-based authentication  
- Access Token + Refresh Token  
- Token type validation (`access` / `refresh`)  
- User-based permission control  

---

## Features

- User registration  
- Login with JWT authentication  
- Token refresh  
- Order creation  
- Order inspection  
- Add items to orders  
- Remove items  
- Finish orders  
- Cancel orders  
- User permission control  

---

## Continuous Integration

This project uses GitHub Actions to automatically validate the backend on every push and pull request.

The CI pipeline includes:

- Setting up a clean Python environment  
- Spinning up a PostgreSQL service  
- Applying database migrations with Alembic  
- Running automated tests with Pytest  

This ensures that the application is always in a working state and prevents regressions.

---

## Running the project with Docker

### 1. Clone the repository

```bash
git clone https://github.com/Lisboa062/PythonFastAPI.git
cd PythonFastAPI
```

### 2. Create `.env` file

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/pythonfastapi
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Recommended: create a `.env` file based on `.env.example`.

---

### 3. Start the environment

```bash
docker compose up -d --build
```

---

### 4. Access the API

```text
http://localhost:8000/docs
```

---

## Migrations

Database migrations are automatically applied at startup using Alembic.

---

## Running tests

```bash
python -m pytest -v
```

Tests cover:

- Authentication  
- Permissions  
- Order lifecycle  
- Error handling  

---

## Database

- PostgreSQL running in Docker  
- Persistent storage using volumes  
- Schema versioning with Alembic  

---

## Test structure

```text
tests/
├── conftest.py
├── test_auth.py
└── test_orders.py
```

---

## Environment configuration

The project uses environment variables via `.env`.

Example:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/pythonfastapi
SECRET_KEY=your_secret_key
```

---

## System startup flow

1. PostgreSQL container starts  
2. Healthcheck validates database readiness  
3. API waits for database  
4. Alembic applies migrations automatically  
5. Uvicorn starts the server  

---

## Future improvements

- Test coverage reporting (pytest-cov)  
- Code quality tools (linting with Ruff / formatting)  
- Logging and observability improvements  
- Cloud deployment (AWS, GCP, or similar)  

---

## Author

Developed by **Wagner Lisboa**

- GitHub: https://github.com/Lisboa062  
- LinkedIn: https://www.linkedin.com/in/lisboa062/  

---

## Final notes

This project was built with the goal of applying modern backend development practices, aiming to simulate a production-ready environment.
