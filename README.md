# Wort-Wirbel API

[![CI/CD Pipeline](https://github.com/akpandeya/wort-wirbel-api/actions/workflows/ci.yml/badge.svg)](https://github.com/akpandeya/wort-wirbel-api/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/akpandeya/wort-wirbel-api/branch/main/graph/badge.svg)](https://codecov.io/gh/akpandeya/wort-wirbel-api)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=akpandeya_wort-wirbel-api&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=akpandeya_wort-wirbel-api)

A FastAPI-based REST API for the Wort-Wirbel application with automated CI/CD, code quality checks, and deployment to Render.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Database Integration**: PostgreSQL database with SQLAlchemy 2 ORM
- **Word Management**: CRUD operations for vocabulary/grammar words
- **Domain-Driven Design**: Clean architecture with domain, application, and infrastructure layers
- **Repository Pattern**: Abstracted data access with interface-based design  
- **Database Migrations**: Alembic for database schema management
- **Comprehensive Testing**: Unit and integration tests with 80%+ coverage
- **Code Quality**: Automated linting with Ruff, formatting, and type hints
- **CI/CD Pipeline**: GitHub Actions for automated testing and deployment

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 🧪 **Comprehensive Testing** - 100% test coverage with pytest
- 🔍 **Code Quality** - Automated linting, formatting, and import sorting with Ruff
- 📊 **SonarQube Integration** - Continuous code quality monitoring
- 🔄 **CI/CD Pipeline** - Automated testing, building, and deployment
- 🌐 **Render Deployment** - Automatic deployment to Render cloud platform
- 📚 **API Documentation** - Interactive OpenAPI/Swagger documentation

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/akpandeya/wort-wirbel-api.git
   cd wort-wirbel-api
   ```

2. **Set up Python 3.13 environment**
   Make sure you have Python 3.13 installed. You can download it from [python.org](https://www.python.org/downloads/).
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   poetry install
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Set up the database (optional)**
   
   If you want to use the database features, start a PostgreSQL instance:
   ```bash
   # Using Docker
   docker run --name postgres-wort-wirbel -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=wort_wirbel -p 5432:5432 -d postgres:15
   
   # Run database migrations
   poetry run alembic upgrade head
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Alternative API docs: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

## API Endpoints

- `GET /` - Hello World endpoint
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Development

### Code Quality

This project enforces strict code quality standards:

- **Ruff** - Linting, formatting, and import sorting
- **pytest** - Testing with coverage

Run quality checks:
```bash
# Lint, format, and sort imports
ruff check app tests
ruff format app tests
ruff check --select I app tests

# Run tests with coverage
pytest --cov=app --cov-report=html
```

### Testing

Run tests:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_main.py -v
```

View coverage report:
```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html
open htmlcov/index.html  # View in browser
```

### Project Structure

```
wort-wirbel-api/
├── app/                    # Application code
│   ├── __init__.py
│   ├── main.py            # FastAPI application and routes
│   ├── domain/            # Domain models and business logic
│   │   └── models.py      # Pydantic domain models (Word, enums)
│   ├── application/       # Use cases and application services
│   │   └── services.py    # Business logic services
│   ├── infrastructure/    # Infrastructure concerns
│   │   ├── config.py      # Configuration management
│   │   ├── database/      # Database setup and SQLAlchemy models
│   │   └── repositories/  # Data access layer
│   └── presentation/      # API layer
│       └── api.py         # FastAPI routes
├── tests/                 # Test files
│   ├── __init__.py
│   ├── test_*.py          # Unit and integration tests
├── alembic/               # Database migrations
│   ├── versions/          # Migration files
│   └── env.py            # Alembic configuration
├── docs/                  # Documentation
│   └── database_schema.md # Database schema documentation
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI/CD pipeline
├── pyproject.toml         # Project configuration
├── poetry.lock            # Poetry lock file (exact dependency versions)
├── alembic.ini           # Alembic migration configuration
├── sonar-project.properties # SonarQube configuration
├── render.yaml           # Render deployment configuration
└── README.md             # This file
```

## CI/CD Pipeline

The project uses GitHub Actions with separate workflows for:

1. **Code Quality Checks** (Ruff)
2. **Testing and Coverage**
3. **Build and API Endpoint Validation**
4. **Deployment** (only after CI passes and only on master)

- All code quality checks run in parallel for fast feedback.
- Tests and build jobs depend on successful code quality checks.
- Deployment to Render is triggered only after CI passes on master.

### Setting up CI/CD

1. **SonarQube Integration**
   - Add `SONAR_TOKEN` to GitHub repository secrets
   - Add `SONAR_HOST_URL` to GitHub repository secrets
   - Configure your SonarQube project with the key `akpandeya_wort-wirbel-api`

2. **Render Deployment**
   - Add `RENDER_SERVICE_ID` to GitHub repository secrets
   - Add `RENDER_API_KEY` to GitHub repository secrets
   - Connect your Render service to this repository

## Deployment

### Render (Recommended)

The application is configured for automatic deployment to Render:

1. **Create a new Web Service** on Render
2. **Connect your GitHub repository**
3. **Use the following settings**:
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Health Check Path: `/health`

4. **Set environment variables** (if needed):
   - `PYTHON_VERSION`: `3.12.3`

The `render.yaml` file in the repository root contains the complete deployment configuration.

## Configuration

### Environment Variables

- `PORT` - Server port (default: 8000)
- `PYTHON_VERSION` - Python version (default: 3.12.3)

#### Database Configuration

- `DB_HOST` - Database host (default: localhost)
- `DB_PORT` - Database port (default: 5432)  
- `DB_NAME` - Database name (default: wort_wirbel)
- `DB_USER` - Database username (default: postgres)
- `DB_PASSWORD` - Database password (default: postgres)

### Application Configuration

The application can be configured via `pyproject.toml`:

- Test configuration and coverage settings
- Code formatting rules (Black)
- Import sorting rules (isort)
- Project metadata

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and ensure all tests pass
4. Run code quality checks: `ruff check app tests && ruff format app tests`
5. Add tests for new functionality
6. Commit your changes: `git commit -am 'Add feature'`
7. Push to the branch: `git push origin feature-name`
8. Create a Pull Request

## Quality Standards

- Minimum 80% test coverage required
- All code must pass Ruff linting, formatting, and import sorting
- SonarQube quality gate must pass

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/akpandeya/wort-wirbel-api/issues) on GitHub.
