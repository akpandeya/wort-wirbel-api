"""
API endpoints for general information and health
"""

from fastapi import APIRouter

from app.application.services import HealthService, InfoService
from app.domain.models import HealthStatus, ServiceInfo

router = APIRouter()


@router.get("/", response_model=ServiceInfo)
async def hello_world() -> ServiceInfo:
    """
    Hello World endpoint

    Returns:
        ServiceInfo: A simple greeting message with service info
    """
    return InfoService.get_service_info()


@router.get("/health", response_model=HealthStatus)
async def health_check() -> HealthStatus:
    """
    Health check endpoint for monitoring

    Returns:
        HealthStatus: Health status
    """
    return HealthService.get_health_status()
