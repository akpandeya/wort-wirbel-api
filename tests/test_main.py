"""
Tests for the main FastAPI application
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello_world():
    """Test the hello world endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello World"
    assert data["service"] == "wort-wirbel-api"
    assert "version" in data


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "wort-wirbel-api"


def test_openapi_docs():
    """Test that OpenAPI docs are accessible"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_json():
    """Test that OpenAPI JSON schema is accessible"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "Wort-Wirbel API"
