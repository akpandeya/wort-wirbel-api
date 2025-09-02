# Wort-Wirbel API

[![CI/CD Pipeline](https://github.com/akpandeya/wort-wirbel-api/actions/workflows/ci.yml/badge.svg)](https://github.com/akpandeya/wort-wirbel-api/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/akpandeya/wort-wirbel-api/branch/main/graph/badge.svg)](https://codecov.io/gh/akpandeya/wort-wirbel-api)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=akpandeya_wort-wirbel-api&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=akpandeya_wort-wirbel-api)

A FastAPI-based REST API for the Wort-Wirbel application with automated CI/CD, code quality checks, and deployment to Render.

## Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 🧪 **Comprehensive Testing** - 100% test coverage with pytest
- 🔍 **Code Quality** - Automated linting with Black, flake8, and isort
- 📊 **SonarQube Integration** - Continuous code quality monitoring
- 🔄 **CI/CD Pipeline** - Automated testing, building, and deployment
- 🐳 **Docker Support** - Containerized application ready for deployment
- 🌐 **Render Deployment** - Automatic deployment to Render cloud platform
- 📚 **API Documentation** - Interactive OpenAPI/Swagger documentation

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/akpandeya/wort-wirbel-api.git
   cd wort-wirbel-api
   ```

2. **Set up Python environment**
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

5. **Access the API**
   - API: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Alternative API docs: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

### Using Docker

1. **Build the Docker image**
   ```bash
   docker build -t wort-wirbel-api .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 wort-wirbel-api
   ```

## API Endpoints

- `GET /` - Hello World endpoint
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Development

### Code Quality

This project enforces strict code quality standards:

- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting and style checks
- **pytest** - Testing with coverage

Run quality checks:
```bash
# Format code
black app tests
isort app tests

# Check linting
flake8 app tests

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
│   └── routers/           # Additional route modules
├── tests/                 # Test files
│   ├── __init__.py
│   └── test_main.py       # Main application tests
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI/CD pipeline
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── pyproject.toml         # Project configuration
├── sonar-project.properties # SonarQube configuration
├── Dockerfile            # Docker container configuration
├── render.yaml           # Render deployment configuration
└── README.md             # This file
```

## CI/CD Pipeline

The project includes a comprehensive GitHub Actions pipeline that:

1. **Code Quality Checks**
   - Runs Black formatter validation
   - Checks import sorting with isort
   - Performs linting with flake8
   - Executes tests with coverage reporting

2. **SonarQube Analysis**
   - Analyzes code quality and security
   - Tracks technical debt and maintainability
   - Enforces quality gates

3. **Build and Test**
   - Tests application startup
   - Validates API endpoints
   - Builds Docker image

4. **Deployment**
   - Automatically deploys to Render on main branch pushes

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

### Manual Docker Deployment

1. **Build and tag the image**:
   ```bash
   docker build -t wort-wirbel-api:latest .
   ```

2. **Run the container**:
   ```bash
   docker run -d -p 8000:8000 --name wort-wirbel-api wort-wirbel-api:latest
   ```

## Configuration

### Environment Variables

- `PORT` - Server port (default: 8000)
- `PYTHON_VERSION` - Python version (default: 3.12.3)

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
4. Run code quality checks: `black app tests && isort app tests && flake8 app tests`
5. Add tests for new functionality
6. Commit your changes: `git commit -am 'Add feature'`
7. Push to the branch: `git push origin feature-name`
8. Create a Pull Request

## Quality Standards

- Minimum 80% test coverage required
- All code must pass Black formatting
- All imports must be sorted with isort
- All code must pass flake8 linting
- SonarQube quality gate must pass

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/akpandeya/wort-wirbel-api/issues) on GitHub.
